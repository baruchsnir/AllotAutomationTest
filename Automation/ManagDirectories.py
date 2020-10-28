import os,shutil
import time

class ManageDirectories:
    def __init__(self, watchDirectory,log):
        self.watchDirectory = watchDirectory
        self.log = log
    def clearWatchDirectory(self):
        if not os.path.exists(self.watchDirectory):
            return
        os.chdir(self.watchDirectory)
        # newpath = os.getcwd()
        # list = os.listdir(self.watchDirectory)
        # for f in list:
        #     if '.' in f:
        #         os.remove(f)
        #         time.sleep(0.3)

        for filename in os.listdir(self.watchDirectory):
            file_path = os.path.join(self.watchDirectory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path):
                #     shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    def clearFilesDirectory(self):
        dir = self.watchDirectory+'/dirty'
        list = []
        if os.path.exists(dir):
            os.chdir(dir)
            newpath = os.getcwd()
            # list = os.listdir(dir)
            # for f in list:
            #     if '.' in f:
            #         os.remove(f)
            #         time.sleep(0.3)
            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        dir = self.watchDirectory+'/clean'
        list.clear()
        if os.path.exists(dir):
            os.chdir(dir)
            newpath = os.getcwd()
            # list = os.listdir(dir)
            # for f in list:
            #     if '.' in f:
            #         os.remove(f)
            #         time.sleep(0.3)
            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        return True
    def TestExistFiles(self,totalFilesGenerate):
        countfiles = 0
        dir = self.watchDirectory+'/dirty'
        if os.path.exists(dir):
            os.chdir(dir)
            newpath = os.getcwd()
            list = os.listdir(newpath)
            countfiles += len(list)
        dir = self.watchDirectory+'/clean'
        if os.path.exists(dir):
            os.chdir(dir)
            newpath = os.getcwd()
            list = os.listdir(newpath)
            countfiles += len(list)
        result =True
        if countfiles < totalFilesGenerate:
            result = False
        return result
