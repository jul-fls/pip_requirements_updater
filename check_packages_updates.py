import os
import requests
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup

automatically_updated_packages = 0
manually_updated_packages = 0
automatically_not_updated_packages = 0
manually_not_updated_packages = 0

def query_pypi(package, version=None):
    url = f"https://pypi.org/project/{package}/"
    if version:
        url += f"{version}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_version_and_release_date(soup):
    pip_command = soup.select_one(".package-header__name").get_text(strip=True)
    latest_version = pip_command.replace(" ", "==").lower()
    release_date_str = soup.select_one(".package-header__date > time")['datetime']
    release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%dT%H:%M:%S%z')
    return latest_version, release_date

def handle_package_update(package, version, pbar):
    soup = query_pypi(package)
    latest_version, latest_release_date = get_version_and_release_date(soup)
    latest_version = latest_version.split('==')[1]
    release_date_str = latest_release_date.strftime('%Y-%m-%d')
    
    if version != latest_version:
        if (today - latest_release_date).days < 7:
            soup = query_pypi(package, version)
            _, previous_release_date = get_version_and_release_date(soup)
            previous_release_date_str = previous_release_date.strftime('%Y-%m-%d')
            delta = latest_release_date - previous_release_date
            
            # Clear the progress bar
            pbar.clear(nolock=True)
            
            question = f"The package {package}=={latest_version} was updated on {release_date_str}, less than a week ago.\nThe currently installed version is {version} and has been released on {previous_release_date_str} ({delta.days} days ago).\nDo you want to proceed with this version? (y/n) "
            user_input = input(question)

            # Redraw the progress bar
            pbar.refresh()
            if user_input.lower() == 'y':
                updated_package_str = f"{package}=={latest_version} # Updated, Latest release date: {release_date_str}"
                global manually_updated_packages
                manually_updated_packages += 1
            else:
                updated_package_str = f"{package}=={version} # Not updated, release date: {previous_release_date_str}"
                tqdm.write(f"Keeping {package}=={version}...")
                global manually_not_updated_packages
                manually_not_updated_packages += 1
        else:
            updated_package_str = f"{package}=={latest_version} # Latest release date: {release_date_str}"
            global automatically_updated_packages
            automatically_updated_packages += 1
    else:
        updated_package_str = f"{package}=={version} # Not updated, latest release date: {release_date_str}"
        global automatically_not_updated_packages
        automatically_not_updated_packages += 1
    
    return updated_package_str

# Rename the current requirements.txt
print("Renaming current requirements.txt to requirements.txt.old...")
os.rename('requirements.txt', 'requirements.txt.old')

# Initialize a new requirements.txt
print("Creating new requirements.txt file...")
with open('requirements.txt', 'w') as f:
    pass

# Get the list of packages
with open('requirements.txt.old', 'r') as f:
    lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    packages = [line.split('==')[0].strip() for line in lines]
    versions = [line.split('==')[1].split('#')[0].strip() for line in lines]

updated_packages = []

# Parse each package's PyPi page and write the latest version to the new requirements.txt
print("Checking for package updates...")
today = datetime.datetime.now(datetime.timezone.utc)  # make today offset-aware in UTC
with tqdm(total=len(packages), desc='Updating packages', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}',ascii="░▒█") as pbar:
    for package, version in zip(packages, versions):
        tqdm.write(f"Updating {package}...")
        updated_packages.append(handle_package_update(package, version, pbar))
        pbar.update()  # Manually update the progress bar after each iteration


# Sort the updated packages
updated_packages.sort()

# Write the sorted packages to the file
with open('requirements.txt', 'w') as f:
    f.write("# This file is automatically generated by check_packages_updates.py\n")
    f.write("# Last updated on " + datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') + "\n\n")
    for package in updated_packages:
        f.write(f"{package}\n")
        
print("\nSummary:")
print(f"Automatically updated packages: {automatically_updated_packages}")
print(f"Manually updated packages: {manually_updated_packages}")
print(f"Automatically not updated packages: {automatically_not_updated_packages}")
print(f"Manually not updated packages: {manually_not_updated_packages}")
print("Done!")
