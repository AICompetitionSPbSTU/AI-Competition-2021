# Analyzing-code-Metrics-2021

Team project to create a code analyzer for the discipline "System programming technology"  

## Commit style  
Format of the main commit:  
1)What to do + for which entity + details (optional)
  
    add ui-bootstrap.js dependency
	replace twitter-bootstrap.css with pure.css
	
2)Additional message - a line away from the main one

	replace twitter-bootstrap.css with pure.css
	Made UI much cleaner.
	
3)Write a message with a small letter

	add ui-bootstrap.js dependency
Instead of

	Add ui-bootstrap.js dependency
	
4)We DON'T use the past tense.
The simpler, the better. The elapsed time makes it too difficult to read messages 

	add ui-bootstrap.js dependency
Instead of

	added ui-bootstrap.js dependency
	
5)Removing unnecessary punctuation marks

Format of the information that goes with the commit  
BEFORE the main commit, we specify the type of the commit:
   1. feature — used when adding new application-level functionality  
   2. fix — if you fixed some serious bug  
   3. docs — everything about the documentation  
   4. style — correcting typos, correcting formatting  
   5. refactor — refactoring the application code  
   6. test — everything related to testing  
   7. chore — normal code maintenance  

And Specify the scope (scope). Immediately after the commit type without any
we specify the area of spaces in parentheses,  
which is covered by our commit.
After that, we write our standard commit.

In addition, for integration with Jira, you need to specify  
COD-(the number of your sub-task).
	
The resulting commits look like: 

	COD-12 refactor(audio-controls) use common library for all controls
	COD-19 chore(Gruntfile.js) add watch task
	
## Code style
Except that we use flake8 instead of pylint,   
we follow the rules of writing code in python from google
  https://google.github.io/styleguide/pyguide.html
  
### Main branch

`main` branch is protected, direct pushes are restricted

Only admins are allowed to directly push to `main` (though it's not recommended anyway)

### Other branches

To contribute a new feature, create a new branch from `main`

There are two allowed types of branches: `feature` and `fix`

Branch type should be separated from name by a backslash, for example, `feature/new-panel` or `fix/blinking-screen`

#### Feature

`feature` branches are used to actually contribute new features

`feature` branch could be created only from `main` and merged only into it

Merging `feature` branch requires creating **pull request** and at least 2 other developers to approve it

It's recommended to tag new **MINOR** version after merging `feature` branch into `main`

#### Fix

`fix` branches could be created and merged from both `main` or `feature`

It's not recommended to create `fix` branch from your own `feature`, but it's likely for other people to branch their `fix` from your `feature`

Merging `fix` also requires **pull request** and *(currently)* 2 other developers to approve it

After merging `fix` branch into `main`, it's highly recommended to tag new **PATCH** version
