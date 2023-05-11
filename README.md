# pip_requirements_updater
A simple requirements.txt updater tool

# Description

## EN
This script simply looks for a "requirements.txt" file in the same folder and create a copy "requirements.txt.old" and for every package it searches if there's a newer version available and if there is it checks if it less than 7 days old and in that case it asks you if you want to update (because it can be too fresh to be reliable), you can choose to update or not and if it's more than 7 days old it will automatically update it in the new "requirements.txt" file and output if the package has been updated or not and timestamps the file with the last update date.

## FR
Ce script recherche simplement un fichier "requirements.txt" dans le même dossier et crée une copie "requirements.txt.old" et pour chaque paquet, il recherche s'il existe une version plus récente et si c'est le cas, il vérifie si elle date de moins de 7 jours et dans ce cas, il vous demande si vous voulez la mettre à jour (parce qu'elle peut être trop récente pour être fiable), vous pouvez choisir de la mettre à jour ou non et si elle date de plus de 7 jours, elle sera automatiquement mise à jour dans le nouveau fichier "requirements.txt" et indiquera si le paquet a été mis à jour ou non et horodatera le fichier avec la date de la dernière mise à jour.
