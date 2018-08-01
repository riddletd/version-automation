# Version Automator

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

1.  Enter a unique version tag into version.py variable at the top fo the code to identify where you want the calculated verion to be placed.
2.  Place the tag into any file in your project. It would be wise to put it somewhere meaningful like package.json or etc...
3.  Make sure version.py is executable (chmod +x version.py)
4.  Run ./version
8.  It will search your files for your unique version tag and replace the tag with the appropriate calculated version in every file it finds a tag.

Note: If you ran this as a test inside your project, please change the calculated version back to your unique version tag! If you don't, your project may never launch again... jk. But really, change it back so Jenkins can add the current version during deployment.
