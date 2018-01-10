+++
title = "Provisioning and deploying this blog with Ansible"
path = "deploying-this-blog-using-ansible"
description = "Showing off Ansible by example"
date = "2013-08-17"
category = "Devops"
tags = ["ansible"]
+++

## Introduction
Making changes by hand on a server is bad practice.    
If you have several servers you might forget to modify all of them, will be time consuming and deploying will be tedious.  
Or you get a new server and need to make it up and running quickly, are you going to remember everything you did on the current servers ?    
  
Fortunately, lots of tools exist to automate the process : Chef, Puppet, Salt, Ansible and several others.
Because I don't want to configure my server everytime and would like to automate the whole deploy thing, I chose to use 
Ansible for it.  
We're also using Ansible for [Hizard](http://www.hizard.com/ "Hizard") as well so there's that. 


## Ansible, I choose you!
I use [Ansible](http://www.ansibleworks.com/ "Ansible") because it's the simplest solution I found.
Playbooks (Ansible terms for the file that contains the actions to do on a server) are in YAML and configuration files in Jinja2 templates.  
You can't get easier than that, no weird custom ruby stuff.  
Also, it works by just SSHing to the servers, unlike the others that require to have a daemons on every servers.  
Lastly, it's written in Python, easy to write modules for and the community is very active.  


## Installation and structure
As Ansible is Python, let's just use a virtual env !  

```bash  
$ mkvirtualenv ansible  
$ pip install ansible
```  

And that's it really.   
  
This is the structure I'm using : 

```bash  
├── development
├── production
├── roles
│   ├── common
│   │   └── tasks
│   │       └── main.yml
│   └── pelican
│       ├── files
│       │   ├── key
│       │   ├── key.pub
│       │   └── known_hosts
│       ├── handlers
│       │   └── main.yml
│       ├── tasks
│       │   ├── deploy.yml
│       │   └── main.yml
│       ├── templates
│       │   └── nginx.conf.j2
│       └── vars
│           └── main.yml
└── site.yml

```

I'll go over these files one by one.  


## Inventories (development, production)
This is where you define the hosts against which you are going to run your playbooks.  
The development file contain only the VM I use to test the playbook and the production one includes the live server.  
Inventory file are simple ini files (there are some specific features you can look at in Ansible doc) :  

```ini
[blog]
192.168.43.157
```

(I'm using ip here but you can use domain name too of course).  
In this file I listed the 192.168.43.157 ip as being part of the blog group.  


## Playbooks (site.yml)
This is the main compononent of Ansible.
site.yml is the master playbook which does both the provisioning and the deploy, you can of course have a playbook specific to provision and one
specific to deploy if you prefer.

```yaml
---

- name: Update Ubuntu, install Pelican, grab the repo, generate the blog
  hosts: blog
  user: root

  roles:
    - common
    - pelican
```
All these lines are worth explaining :

- name: describe what the playbook or task (details on tasks below) does
- hosts: which group the playbook should be run against
- user: which user you want to connect and run the playbook with (Ansible defaults to the user running the playbook, which is rarely what you want)
- roles: this is new in Ansible 1.2. Roles are basically meant to divide a playbook in small subsets to make it more reusable and clear


## Roles (everything in roles/directory)
Roles are basically directories containing known directories: tasks, files, templates, handlers and vars.  
All the main.yml in these folders will automatically be added to the play and you won't need to specify path for files in files and templates. 


## Tasks (roles/\*/tasks/\*.yml) 
These are the actions the play will execute
Here's the roles/pelican/tasks/main.yml :

```yaml
---

- name: Install required system packages.
  apt: pkg={{ item }} state=installed
  with_items: '{{ packages }}'

- name: Create user
  user: home={{ user_home }} name={{ user }} shell=/bin/bash state=present

- name: Add user to sudo group
  user: name={{ user }} groups=sudo append=true

- name: Create the SSH directory.
  file: state=directory path={{ user_ssh_directory }}

- name: Upload SSH known hosts.
  copy: src=known_hosts dest={{ user_ssh_directory }}known_hosts mode=0600

- name: Upload SSH private key.
  copy: src=key dest={{ user_ssh_directory }}id_rsa mode=0600

- name: Add authorized key for the user
  authorized_key: user={{ user }} key='{{ item }}'
  with_file:
    - key.pub

- name: Change permissions
  shell: chown -R {{ user }}:{{ user }} {{ user_home }}

# Deploy is in a different file because it might get long

- include: deploy.yml
```

This uses several [modules](http://www.ansibleworks.com/docs/modules.html "Ansible modules") but this is really how Ansible works : give a 
name to a task and the command to execute, using a module or a raw command.     
I include the deploy.yml instead of listing the tasks in main.yml because I might want to create another playbook only for deploy and it's clearer 
that way anyway.  
All the {{ }} elements are variables explained in the next part.  
Since you probably don't want to run the whole play everytime you're deploying something, you can tag some tasks and run tasks by tags later.  
Here is the deploy.yml :

```yaml
---

# Deploy part of the playbook

- name: Pull source from bitbucket
  git: repo={{ repo }} dest={{ blog_directory }}
  sudo: yes
  sudo_user: '{{ user }}'
  tags: 
    - deploy

- name: Init submodules
  command: git submodule update --init --recursive chdir={{ blog_directory }}
  sudo: yes
  sudo_user: '{{ user }}'
  tags: 
    - deploy

- name: Install requirements
  pip: requirements={{ blog_directory }}requirements.txt virtualenv={{ user_home }}env
  sudo: yes
  sudo_user: '{{ user }}'
  tags:
    - deploy

- name: Generate blog
  shell: . {{ user_home }}env/bin/activate && make publish chdir={{ blog_directory }}site
  sudo: yes
  sudo_user: '{{ user }}'
  tags:
    - deploy

- name: Copy nginx config (as I might add some custom stuff for some urls)
  template: src=nginx.conf.j2 dest=/etc/nginx/sites-enabled/{{ user }}
  notify: reload nginx
  tags:
    - deploy
```
Several things going on there.  
First you can notice that we're using sudo and sudo_user because we want to run these steps as the pelican user and not root (not very satistied 
of that solution, would probably make more sense to have a deploy role using the pelican user directly).  
All the tasks are using the deploy tag, meaning that I will be able to run only those tasks later if I choose to.


## Variables (roles/\*/vars/\*.yml)
These values will be added into the play and usable throughout the play.  
In this case, I'm using the variables in tasks and templates (the nginx config).  
You can also define variable specific to a group by putting them in a group_vars folder in a top directory and naming the yml file the name of the 
group (or use all.yml if you want the variables to be available for every groupe).  
You can use interpolation from within the file itself, but you need to use the ${} syntax of the {{ }} (if anyone knows how to make it work using {{ }} ).

```yaml
---

user: pelican
user_home: /home/${user}/
user_ssh_directory: ${user_home}.ssh/
blog_directory: ${user_home}blog/
serve_directory: ${blog_directory}site/output/

repo: git@bitbucket.org:Keats/perso.git

packages:
  - build-essential
  - python2.7-dev
  - git
  - fail2ban
  - python-virtualenv
  - nginx
```


## Handlers (roles/\*/handlers/\*yml)
Handlers are tasks that you reference by name (you can see the notify: reload nginx in the deploy.yml).  
They are basically used to restart/reload services.

```yaml
---

- name: reload nginx
  service: name=nginx state=reloaded
```


## Running it
To run a playbook, just specify which inventory file you want to use with -i flag and the name of the playbook file.
If you're logging in with a password, you will need the --ask-pass option.  
You can also limit which tasks should be run using the tags parameter.

```bash
$ ansible-playbook --ask-pass -i development site.yml
$ ansible-playbook --ask-pass -i development site.yml --tags "deploy"
```


### Conclusion
Having the whole process automated means I can get a new server and have it up and running in less than 5 minutes and that's pretty cool.  
I'm also going to put the deploy in the post-commit hook so I won't even have to run the playbook manually.    
