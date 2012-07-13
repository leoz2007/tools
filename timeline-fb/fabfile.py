from __future__ import with_statement
from fabric.api import local, settings, abort, run, env
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed
from fabric.contrib.project import rsync_project
from fabric.context_managers import cd, settings, hide
from fabric.operations import put
import re
import os, sys
import ConfigParser
import time

APPSFOLDER="/opt/djangoapps/"
WSGI_SUPERCONF = os.path.join(APPSFOLDER, 'django_base')
SUBSCRIPTION_FILE = APPSFOLDER + 'domains.txt'
env.use_ssh_config = True
CELERY_CONF_FILE = 'celery.conf'
env.hosts = ["jibli_dev"]


### GET GLOBAL REPO CONFIG
with settings(
        hide('warnings', 'running', 'stdout', 'stderr')
        ):
    GITURL = local("git config remote.origin.url", capture=True)
    if GITURL.failed:
        abort("Error: Unable to get the git REPOsitory. Are you running the script from a git project?")
    GITURL = re.sub(r'^.+:', 'git@github.com:', GITURL)
    REPO = GITURL.split(":")[1].split("/")[1].split(".")[0]
    BRANCH = local("git branch", capture=True)
    if BRANCH.failed:
        abort("Error: Unable to get the git branch. Are you running the script from a git project?")
    BRANCH = BRANCH.split("\n")
    for b in BRANCH:
        if b.startswith("* "):
            BRANCH = b[2:]
            break
    if BRANCH == "(no BRANCH)":
        abort("You must be on a valid BRANCH to run the script.")

    APPFOLDER = os.path.join(APPSFOLDER, '%s-%s' % (REPO, BRANCH))
    DJANGO_FOLDER = os.path.join(APPFOLDER, 'app')
    APP_VENV = os.path.join(APPFOLDER, 'virt')
    CELERY_DIR = DJANGO_FOLDER


def dev():
    '''Run commands on dev server'''
    env.hosts = ["jibli_dev"]

def qm():
    '''quick_merge'''
    quick_merge()

def quick_merge(force="n", verbose="f"):
    '''Runs git pull --rebase and merge with dev'''
    if confirm('Make sure to git pull --rebase origin dev and you have a clean working tree before continuing'):
        BRANCH = local("git branch", capture=True)
        BRANCH = BRANCH.split("\n")
        for b in BRANCH:
            if b.startswith("* "):
                BRANCH = b[2:]
                break
        if BRANCH == "(no BRANCH)":
            abort("You must be on a valid BRANCH to run the script.")
        local('git stash')
        local('git checkout dev; git merge %s;git push origin dev; git checkout %s' % (BRANCH, BRANCH))
        local('git stash pop')

def restart():
    '''Restart app'''
    run('touch %s' % (os.path.join(APPFOLDER, '%s-%s.ini' % (REPO, BRANCH))))
    time.sleep(5)
    update_tasks()

def update_dependencies():
    '''Update app dependencies from "dependencies.txt"'''
    with cd(DJANGO_FOLDER):
        ret = run('exec %s install -r dependencies.txt' % os.path.join(APP_VENV, 'bin/pip'))
        if ret.failed:
            abort('Error: could not install dependencies.txt, make sure it exists on your branch')

def pyshell():
    '''Launches manage.py shell in the remote app'''
    with cd(DJANGO_FOLDER):
        run('%s manage.py shell' % os.path.join(APP_VENV, 'bin/python'))

def mongo():
    '''Launches a mongo console on remote app'''
    ## Magic command to make auto closing ssh tunnel
    local('ssh -f -L 27042:localhost:27017 %s sleep 5' % env.hosts[0])
    ## Connect to mongo through local mongo
    local('mongo localhost:27042/%s-%s' % (REPO,BRANCH))

def test_push():
    '''Push local copy of files without git commit or push'''
    rsync_project(remote_dir=DJANGO_FOLDER, local_dir='./', 
            exclude=['.git', 'static', 'settings.py'])
    _activate_deploy_mode()


def push():
    '''Git push local commits, update and restart remote app'''
    print 'git push'
    local('git push origin %s' % BRANCH)

    print 'Remote pull'
    with cd(DJANGO_FOLDER):
        ret = run('git fetch origin;git checkout %s;git reset --hard origin/%s' % (BRANCH, BRANCH))
        _activate_deploy_mode()
        restart()

def deploy(force="n", verbose="f"):
    '''Full deploy of a fresh new app'''
    if confirm('This is gonna take some time are you sure you want to deploy ? you might just want to update'):
        _create_app_folder()
        _check_clean_git()
        _clone_current_ref_to_remote()
        _create_venv()
        update_dependencies()
        _add_celery()
        _start_app()

def ls_logs():
    '''Show available app logs'''
    with settings(
            hide('warnings', 'running', 'stderr', 'stdout'),
            warn_only=True
            ):
        ret = run("ls %s | sed -e 's/\.[a-xA-Z]*$//'" % os.path.join(APPFOLDER, 'log'))
        print ret

def tail_log(logfile):
    '''Executes tail -f on given :logfile'''
    run('tail -f %s' % os.path.join(APPFOLDER, 'log/%s.log' % logfile))

def update_tasks():
    '''Update celery tasks on remote app'''
    run('supervisorctl restart celery-%s-%s' % (REPO,BRANCH))


    return True


## PRIVATE FUNCTIONS

def _activate_deploy_mode():
    sed(os.path.join(DJANGO_FOLDER, 'settings.py'), 'DEPLOY_MODE = False', 'DEPLOY_MODE = True')


def _start_app():
    print 'Starting application'
    _activate_deploy_mode()
    run('cp %s %s' % (WSGI_SUPERCONF, os.path.join(APPFOLDER, '%s-%s.ini' % (REPO,BRANCH))))

def _create_app_folder():
    print "Creating remote folders ..."

    if exists(APPFOLDER) == True:
        if confirm("Error: A project with the same name already exists in " + APPSFOLDER + ". Do you wish to erase it?"):
            run("rm -rf "+ APPFOLDER)
        else:
            abort("Aborting...")
    for f in ["virt", "log", "run", "app"]:
        with settings(warn_only=True):
            ret = run("mkdir -p " + APPFOLDER + "/" + f)
        if ret.failed:
            abort("Error: Unable to create the folder " + APPFOLDER + "/" + f)

def _check_clean_git():
    print "Checking if data to commit..."
    with settings(warn_only=True):
        ret = local("git status -s -uno", capture=True)
        print ret
    if ret.failed and not confirm("Error: Unable to run `git status`. Do you want to continue without commiting?"):
            abort("Aborting...")
    if ret:
        if not confirm("You have some uncommitted changes in your local BRANCH. Do you wish to continue anyway?"):
            abort("Aborting... Please commit and push your changes before running agin");

def _clone_current_ref_to_remote():
    print "Cloning repo on the server..."
    with cd('%s' % APPFOLDER):
        ret = run('git clone %s %s' % (GITURL, 'app'))
        if ret.failed:
            abort("Error: Unable to clone the REPOsitory.")
    print "Checking out the BRANCH on the server..."
    with cd(DJANGO_FOLDER):
        with settings(warn_only=True):
            ret = run('git checkout %s' % BRANCH)
            if ret.failed:
                abort("Error: Unable to checkout to branch %s" % BRANCH)

def _create_venv():
    print 'Creating virtual environments on project directory/virt and installing dependencies'
    ret = run('virtualenv --distribute --no-site-packages %s' % APP_VENV)
    if ret.failed:
        abort('Error: unable to create virtualenv')

def _add_celery():
    '''Adds a celery async task pool daemon to the app'''
    config = ConfigParser.SafeConfigParser()
    section = 'program:celery-%s-%s' % (REPO, BRANCH)
    config.add_section(section)
    PATH = os.path.join(APPFOLDER, 'virt/bin')
    options = {
            'environment': 'PYTHONPATH=%s, DJANGO_SETTINGS_MODULE=settings, PATH=%s' %
                            (DJANGO_FOLDER, PATH),
            'command': 'python manage.py celeryd --loglevel DEBUG -c1',
            'directory': CELERY_DIR,
            'user': 'jibli',
            'numprocs': '1',
            'stdout_logfile': os.path.join(APPFOLDER, 'log/celery.log'),
            'stderr_logfile': os.path.join(APPFOLDER, 'log/celery_error.log'),
            'autostart': 'true',
            'autorestart': 'true',
            'startsecs': '10'
            }

    for k, v in options.iteritems():
        config.set(section, k, v)

    with open(CELERY_CONF_FILE, 'wb') as celeryfile:
        config.write(celeryfile)
    put(CELERY_CONF_FILE, DJANGO_FOLDER)
    local('rm %s' % CELERY_CONF_FILE)
    run('supervisorctl update')
