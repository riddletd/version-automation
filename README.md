# Version Control Automator

This program is meant to automate versioning.

## Dependencies

- python 3

## How to use

This program uses "git flow"-like branch names to calculate the version of a project. It looks for hotfixes, features, and releases to increment the version. The following terms and definitions represent the same thing. In other words, they can be used interchangeably in conversation to represent the same concept. For example, "Concept - Idea - An image in the mind."

- Major - Release - An addition that is NOT backwards compatible.
- Minor - Feature - An addition that is backwards compatible.
- Patch - Hotfix - Bugfix - To fix undesired behavior from a feature or release.

Your branch names should look like this:

```
hotfix/description-of-hotfix
feature/description-of-feature
release/description-of-release
```

1.  Create or use an existing file, such as package.json, to place the calculated version of your project.
2.  Enter a unique version tag to identify where you want the calculated verion to be placed.
3.  Make sure version.py is executable (chmod +x version.py)
4.  Run ./version
5.  Copy and paste the file path of the file you are using into the input.
6.  Copy and paste your unique version tag identifier into the input.
7.  Hit enter.
8.  It should print the version it calculated, and replace your tag with the appropriate value.

Note: If you ran this as a test inside your project, please change the calculated version back to your unique version tag! If you don't, your project may never launch again... jk. But really, change it back so Jenkins can add the current version during deployment.
