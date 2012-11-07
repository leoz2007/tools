from __future__ import with_statement
from fabric.api import local, settings, abort, run, env
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, sed
from fabric.contrib.project import rsync_project
from fabric.context_managers import cd, settings, hide
from fabric.operations import put
import re, getpass
import os, sys
import ConfigParser
import time, datetime, socket

'''
Fabfile for fb-timeline project
'''

APP_ROOT = "/opt/cover/"
SUPERVISOR_APP = "cover"
env.hosts = ["redmine"]
env.use_ssh_config = True


### GET GLOBAL REPO CONFIG
with settings(
        hide('warnings', 'running', 'stdout', 'stderr')
        ):
    GITURL = local("git config remote.origin.url", capture=True)
    if GITURL.failed:
        abort("Error: Unable to get the git repository. Are you running the script from a git project?")
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

    DJANGO_FOLDER = os.path.join(APP_ROOT, 'app')
    APP_VENV = os.path.join(APP_ROOT, 'virt')


#def redmine():
#    '''Run commands on redmine server'''

#    env.hosts = ["redmine"]
    
#def qm():
#    '''quick_merge'''
#    quick_merge()

# def quick_merge(force="n", verbose="f"):
#     '''Runs git pull --rebase and merge with dev'''
#     if confirm('Make sure to git pull --rebase origin dev and you have a clean working tree before continuing'):
#         BRANCH = local("git branch", capture=True)
#         BRANCH = BRANCH.split("\n")
#         for b in BRANCH:
#             if b.startswith("* "):
#                 BRANCH = b[2:]
#                 break
#         if BRANCH == "(no BRANCH)":
#             abort("You must be on a valid BRANCH to run the script.")
#         local('git stash')
#         local('git checkout dev; git merge %s;git push origin dev; git checkout %s' % (BRANCH, BRANCH))
#         local('git stash pop')

def restart():
    '''Restart app'''
    run("supervisorctl restart %s" % SUPERVISOR_APP)

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

#def mongo():
#    '''Launches a mongo console on remote app'''
#    ## Magic command to make auto closing ssh tunnel
#    local('ssh -f -L 27042:localhost:27017 %s sleep 5' % env.hosts[0])
#    ## Connect to mongo through local mongo
#    local('mongo localhost:27042/%s-%s' % (REPO,BRANCH))

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
        _start_app()

def ls_logs():
    '''Show available app logs'''
    with settings(
            hide('warnings', 'running', 'stderr', 'stdout'),
            warn_only=True
            ):
        ret = run("ls %s | sed -e 's/\.[a-xA-Z]*$//'" % os.path.join(APP_ROOT, 'log'))
        print ret

def tail_log(logfile):
    '''Executes tail -f on given :logfile'''
    run('tail -f %s' % os.path.join(APP_ROOT, 'log/%s.log' % logfile))

def add_ip():
    '''Add my external ip address to nginx white list'''
    #myip = local("wget -q -O - checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//'", capture=True)
    myip = local("curl checkip.dyndns.org|sed -e 's/.*Current IP Address: //' -e 's/<.*$//'", capture=True)
    username = getpass.getuser()
    date = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M")
    hostname = socket.gethostname()
    run("echo 'allow %s; # added by %s on %s for host %s' >> /etc/nginx/white_list/jibli" % (myip, username, date, hostname))
    run("sudo /etc/init.d/nginx reload")

## PRIVATE FUNCTIONS

def _activate_deploy_mode():
    sed(os.path.join(DJANGO_FOLDER, 'settings.py'), 'DEPLOY_MODE = False', 'DEPLOY_MODE = True')
    sed(os.path.join(DJANGO_FOLDER, 'settings.py'), 'DEBUG = True', 'DEBUG = False')


def _start_app():
    print 'Starting application'
    _activate_deploy_mode()
    run("supervisorctl restart %s" % SUPERVISOR_APP)

def _create_app_folder():
    print "Creating remote folders ..."

    if exists(APP_ROOT) == True:
        if confirm("Error: The folder '%s' already exists. Do you wish to erase it?" % APP_ROOT):
            run("rm -rf %s" % APP_ROOT)
        else:
            abort("Aborting...")
    for f in ["virt", "log", "run", "app"]:
        with settings(warn_only=True):
            ret = run("mkdir -p " + APP_ROOT + "/" + f)
        if ret.failed:
            abort("Error: Unable to create the folder " + APP_ROOT + "/" + f)

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
    with cd('%s' % APP_ROOT):
        ret = run('git clone %s %s' % (GITURL, 'app'))
        if ret.failed:
            abort("Error: Unable to clone the Repository.")
    print "Checking out the BRANCH on the server..."
    with cd(DJANGO_FOLDER):
        with settings(warn_only=True):
            ret = run('git checkout %s' % BRANCH)
            if ret.failed:
                abort("Error: Unable to checkout to branch %s" % BRANCH)

def _create_venv():
    print 'Creating virtual environments on project directory/virt and installing dependencies'
    ret = run('virtualenv %s' % APP_VENV)
    if ret.failed:
        abort('Error: unable to create virtualenv')
