# General setup

This Repository is based on Discord bots hosted on [Replit](https://www.replit.com).

Offering **helpful features** serving game assisting and alliance/guild organizing tasts for *Rise of Empire* as well as **fun features** to keep everyone entertained.

## Replits

1) **Alfred 2.0** - checked out the *main* branch and is the productive version of the bot running 24/7.
2) **Alfred-dev** - can check out any develop branch to develop features, fix bugs or test stuff. It runs on a different Discord test server so it cannot brake anything. 
3) Possibly have another **Alfred-dev** version on a 3rd repo so 2 people can work independently on stuff without conflicting with each other.

## Branches

There is a main branch which should just have tested and ready for production use features included. 

The develop branch is the starting point for any new development and should be used to branch of feature and bugfix branches. Merge the develop into the main branch whenever you want/can publish new features or bugfixes. 

All code changes should be done in a extra created branch for it an never just be done on the develop or the main. This will help to have those 2 branches always working and not littered with unfinished features or buggy code.


# Workflow

1) Create an issue with your **feature** or **bug**, alternativly choose an existing one to work on.
2) Assign the issue to yourself
3) Create a branch for this issue with base branch *develop* (if no other branch is appropriate)
4) Checkout this branch in one of the development Alfred bots
5) Work on the issue and commit the changes whenever you leave the PC so it is saved.
6) Once feature complete and tested you can create a pull request to merge your branch back to develop
7) If no conflicts just approve the pull request. If unsure ask for a review and if some conflicts occure check those.
8) You can delete the old branch once merge is successful (can be restored if needed)

From time to time or when you want a feature on main branch, merge the develop to main.
