# pip_requirements_updater
A simple requirements.txt updater tool

It simply looks for a "requirements.txt" file in the same folder and create a copy "requirements.txt.old" and for every package search if there's a newer version available and if there is it checks if it less than 7 days old and in that case it asks you if you want to update (because it can be too fresh to be reliable), you can choose to update or not and if it's more than 7 days old it will automatically update it in the new requirements.txt file and output if the package has been updated or not and timestamps the file with the last update time
