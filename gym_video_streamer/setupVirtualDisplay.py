import platform

def installer(packages):
    try:
        import apt
        import apt.debfile

        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.commit()
        for package in packages:
            pkg = cache[package]
            if pkg.is_installed:
                print(f"{package} is already installed !")
            else:
                print(f"Installing {package} ...")
                pkg.mark_install()
        cache.commit()
    except Exception as e:
        print("Exception :: {}".format(e))
        print("-"*100)
        print("Got an exception while installing following [{}] list of packages.".format(" ".join(packages)))


# Setup the virtual display so it doesn't gives error on Google Colab
def set_pyvirtualdisplay():
    try:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1400, 900))
        display.start()
    except Exception as e:
        print("Exception :: {}".format(e))
        print("-"*100)
        print("Got an exception while setting-up the py virtual display.")


def SetupVirtualDisplay(force=False):
    if force is False:
        # Stop the exec for Windows OS & macOS
        system = platform.system()
        if system in ["Windows", "Darwin", "Java"] is not None:
            print("You are using {} platform & this Virtual Display Setup is only required for Google Colab!\n\
            You have to install ffmpeg manually from 'https://ffmpeg.org/download.html'".format(system))
            return
    else:
        # pyvirtualdisplay depends on xvfb
        installer(packages=["ffmpeg", "xvfb"])
        print("Installed all the required packages.")
        set_pyvirtualdisplay()
        print("Virtual Display Setup complete!")


# ---- Note ----

# :: For all OS ::
# On Google Colab display is not there, so thats why pyvirtualdisplay is used to create one virtually.
# But NO need to setup the virtual display unless you have one.
# And you have to install ffmpeg manually from https://ffmpeg.org/download.html


# :: For Linux OS with Display ::
# You don't have to setup the virtual display.
