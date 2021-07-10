# sublime-patcher
Bash script for patching/cracking Sublime Text on Linux including newest build 4107

## Usage
### Patching (cracking)
1. Clone repository
2. Add exec rights to the scrpt if needed
```bash
chmod +x ./sublime_patch.sh
```
3. Run script with superuser privileges
```bash
sudo ./sublime_patch.sh
```
4. Done

<details>
  <summary>Screenshots</summary>

  ![Patching proccess](https://i.imgur.com/xv2c223.png)
  ![Patching result](https://i.imgur.com/3SiVRqu.png)

</details>

### Removing patches
You have an option to remove patches and rollback to the original Sublime Text state.
In order to do that you need to run script again and choose "Restore from backup" option.


<details>
  <summary>Screenshots</summary>

  ![Restoring process](https://i.imgur.com/5Wjl3cq.png)
  ![Restoring result](https://i.imgur.com/TkKC4FE.png)

</details>
