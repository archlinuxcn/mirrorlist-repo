# How to Apply Mirror of Arch Linux CN Repository

We welcome capable organizations and individuals to apply mirror of our software repository. This can improve the performance and reliability of our software distribution, and also provide a better service for the users in your region. To apply, please follow these steps:

1. Clone this repository and edit [mirrors.yaml](mirrors.yaml) with your mirror information. By following the directive `python manager.py all`, the protocols and coordinates fields will be automatically populated, and README.md, archlinuxcn-mirrorlist, and mirrors.geojson files will be generated.

2. Create a pull request with your changes and describe your situation. Please provide an email address for contact.

3. Wait for our email with the rsync username and password. Use the following command to synchronize your mirror with our main server:

   ```bash
   RSYNC_PASSWORD=<your rsync password> rsync --recursive --times --links --hard-links --safe-links --max-delete=1000 --delete-after --delay-updates --itemize-changes --verbose --contimeout=60 <your rsync username>@sync.repo.archlinuxcn.org::repo .
   ```

4. Once your mirror has been initialized, we will merge your pull request and include your mirror in our mirrorlist.

5. We recommend synchronizing every 6 or 7 hours, and avoiding the time when our automatic packaging system, [lilac](https://github.com/archlinuxcn/lilac), is working at 4, 12 and 20 (Asia/Shanghai, UTC+8) every day. This can prevent potential conflicts and errors during the synchronization process.

Alternatively, you can email <repo@archlinuxcn.org> to apply for mirror. We will reply as soon as possible.

Thank you for your support and contribution!
