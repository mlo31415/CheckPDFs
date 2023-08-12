from tkinter import filedialog
from tkinter import *
import os
from PyPDF2 import PdfReader
from PyPDF2 import errors as PyPDF2errors

from Log import LogOpen, Log, LogError


def main():
    root=Tk()
    root.withdraw()
    startpath=filedialog.askdirectory(title="Select root of directory tree to be scanned.", mustexist=True)
    if len(startpath) == 0:
        return

    LogOpen("PDFs with no text")

    startAt=0       # Skip this many PDFs before starting the search
    pdfsScanned=0
    for rootpath, dirs, files in os.walk(startpath, topdown=False):
        for name in files:
            _, extension = os.path.splitext(name)
            if extension.lower() == ".pdf":
                pdfsScanned+=1

                if pdfsScanned < startAt:   # Skip startAt PDFs before actually doing anything
                    continue

                pathname=os.path.join(rootpath, name)
                #pathname="D:/fanac.org backups/fanac.org 2023-07-30/public_html/fanzines/Catch_Trap/catch_trap_89_bradley_1960-02_fapa_90.pdf"
                rootlesspathname=pathname.removeprefix(startpath)

                # open the pdf file
                try:
                    file_in=open(pathname, 'rb')
                    object=PdfReader(file_in)
                except PyPDF2errors.PdfReadError:
                    LogError(f"{rootlesspathname} PdfReader() failed with PdfReadError")
                    continue
                except ValueError:
                    LogError(f"{rootlesspathname} PdfReader() failed with ValueError")
                    continue
                except BaseException:
                    LogError(f"{rootlesspathname} PdfReader() failed with BaseException (whatever that means!)")
                    continue

                try:
                    NumPages=len(object.pages)
                except PyPDF2errors.DependencyError:
                    LogError(f"{rootlesspathname} getNumPages() failed with DependencyError")
                    continue
                except PyPDF2errors.PdfReadError:
                    LogError(f"{rootlesspathname} getNumPages() failed with PdfReadError")
                    continue
                except PyPDF2errors.RecursionError:
                    LogError(f"{rootlesspathname} getNumPages() failed with RecursionError")
                    continue

                if pdfsScanned%50 == 0:
                    Log(f"*********{pdfsScanned} PDFs scanned; working on directory {rootpath}")

                # extract text and do the search
                text=""
                for i in range(0, NumPages):
                    PageObj=object.pages[i]
                    try:
                        text+=PageObj.extract_text()
                    except TypeError:
                        LogError(f"{rootlesspathname} getPage(i) failed with TypeError")
                        break

                    if "fan" in text or "Fan" in text:
                        break

                if "fan" not in text and "Fan" not in text:
                    Log(f"{rootlesspathname}  -- fan not found!  Length is {len(text)} characters")


if __name__ == "__main__":
    main()


