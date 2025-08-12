# Infrastructure Application Version
If using medial::io::ProgramArgs_base wrapper class instead of ProgramArgs of boost you get several things:
You get "help", option to load all arguments form file using --base_config and more..
Running our apps with** --debug** will print the app version and **--version** will just output the application version and exit.

- To compile all our tools with version info use build scripts in Scripts Repo: $MR_ROOT/Projects/Scripts/Bash-Scripts/full_build.sh
- Another option is to compile with

```bash
smake_rel.sh "Version\ comment\ string\ each\ space\ is\ escaped"
```
will compile our program with this comment in version\debug

- example of version output running: bootstrap --version with full_build.sh
*Version Info:*
*Build on 14-01-2019_17:42:20*
*=>Libs Git Head: 8fdbf55f32fc550420f300d391c88295bcb3a46a by avi at 2019-01-14*
*Last Commit Note: pushing the correct val in the diabetes registry*
*=>Tools Git Head: 97e7e06988a606781dda39625507d9702e146ac9 by avi at 2019-01-14*
*Last Commit Note: a diabetes read code list capabale of working with a registry rep processor*
