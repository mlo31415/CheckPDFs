from tkinter import filedialog
from tkinter import *
import os
import PyPDF2

from Log import LogOpen, Log, LogError


def main():
    root=Tk()
    root.withdraw()
    startpath=filedialog.askdirectory(title="Select root of directory tree to be scanned.", mustexist=True)
    if len(startpath) == 0:
        return

    LogOpen("PDFs with no text")

    pdfsScanned=0
    for rootpath, dirs, files in os.walk(startpath, topdown=False):
        for name in files:
            _, extension = os.path.splitext(name)
            if extension.lower() == ".pdf":
                pdfsScanned+=1
                pathname=os.path.join(rootpath, name)
                rootlesspathname=pathname.removeprefix(startpath)

                # open the pdf file
                try:
                    object=PyPDF2.PdfFileReader(pathname)
                except PyPDF2.errors.PdfReadError:
                    LogError(f"{rootlesspathname} PdfFileReader() failed with PdfReadError")
                    continue
                except ValueError:
                    LogError(f"{rootlesspathname} PdfFileReader() failed with ValueError")
                    continue

                try:
                    NumPages=object.getNumPages()
                except PyPDF2.errors.DependencyError:
                    LogError(f"{rootlesspathname} getNumPages() failed with DependencyError")
                    continue
                except PyPDF2.errors.PdfReadError:
                    LogError(f"{rootlesspathname} getNumPages() failed with PdfReadError")
                    continue


                # extract text and do the search
                text=""
                for i in range(0, NumPages):
                    PageObj=object.getPage(i)
                    try:
                        text+=PageObj.extractText()
                    except TypeError:
                        LogError(f"{rootlesspathname} getPage(i) failed with TypeError")
                        break
                    if len(text) > 500:
                        break

                if len(text) < 500:
                    Log(f"{pathname}  --  {len(text)} characters")

                if pdfsScanned%500 == 0:
                    Log(f"{pdfsScanned} PDFs scanned; working on directory {rootpath}")


if __name__ == "__main__":
    main()


