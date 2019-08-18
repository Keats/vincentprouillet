+++
title = "Storing secrets in a git repository with git-crypt"
description = "It is possible to store secrets securely in a git repository; here's how"
+++

One of the most common issues working on a web service is where to store your secrets. When just starting, it's likely that
they will be directly in the repository itself whether it happens accidentally or not. Having your production secrets
 in the clear in the repository is obviously a bad thing and all those secrets should be rotated.

There are multiple ways to store your secrets securely:

- store them in the environment of the servers like Heroku/Aptible do
- store them as CI/CD variables like in Gitlab and bake them in Docker images
- use tools like [Vault](https://www.vaultproject.io/)

If you are on a PaaS with an easy way to set secrets as environment variables, you can stop reading this article and just use that.

However, if you're a small team using a more traditional deployment encrypting secrets in the repository itself is worth
considering. [git-crypt](https://github.com/AGWA/git-crypt) can be used for that. To quote the repository:

> git-crypt enables transparent encryption and decryption of files in a git repository. 
> Files which you choose to protect are encrypted when committed, and decrypted when checked out.

[git-crypt](https://github.com/AGWA/git-crypt) is available through many package managers.

Once you have `git-crypt` and are in your repository, run `git-crypt init` to generate a key. 

The next step is to create a `.gitattributes`, a file similar to `.gitignore`, with the following content:

```gitignore
secrets/**/* filter=git-crypt diff=git-crypt
```

This means that everything inside a folder named `secrets` will be encrypted. It is recommended to use the `**/*` approach as
it would be easy to forget to encrypt some files otherwise.
Now that your `.gitattributes` file is in place, you can start adding secrets in that folder. Since you have the secrets
already unlocked, you will see the file in your `git diff` or `git show`. If you push it to a remote repository and try
to view a file in that directory using the web browser for example, you will notice they are just binary data. Anyone getting access
to the repository will not be able to see them unless they can unlock git-crypt. That also includes you working from
a different computer or your team members.

Clearly, we need to be able to unlock the secrets in more than one computer. There are two ways to go about it:

- GPG
- creating a symmetric key

You can read more about the GPG on the [git-crypt's README](https://github.com/AGWA/git-crypt#using-git-crypt), I will use the symmetric
key for this article.

Here's how you generate a symmetric key:

```
$ git-crypt export-key /path/to/output/file
```

This will generate a binary key that, after `base64`'ing, can be stored in your password manager for example and shared securely
with team mates. And that's where the issue with this approach lies: some people might store the key insecurely which would be 
equivalent to storing your secrets in the clear.

For a small team that can be trusted however, this is an easy approach that can work for quite some time! 