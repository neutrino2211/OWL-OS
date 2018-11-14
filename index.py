#@owldoc

'''@
This file begins the main ui and handles all fatal errors
@'''

import init
prompt = '''
A catastrophic error occured and your computer is having a hard time booting.
This might be caused by a device malfunction or the startup disk is corrupted.
Two options are available to try and recover the system
    1: Restart
    2: Re-install (will wipe data)
    3: shutdown
> '''
def main():
    try:
        init.init()
    except Exception as e:
        init.graceful_exit()
        import traceback
        print(traceback.print_exception(*init.sys.exc_info()))
        print("Fatal error!!")
        v = input(prompt)
        if v=='1':
            main()
        elif v=='3':
            init.sys.exit(0)
        else:
            import install
            install.main(install.args)
            main()
    except Exception:
        # Extremely fatal error
        print("ERROR")

main()
if not init.shutdown:
    init.graceful_exit()