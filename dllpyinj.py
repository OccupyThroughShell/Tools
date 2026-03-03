import sys
import os
import ctypes
from ctypes import wintypes
from ctypes import *
#Windows Constants
"""
PAGE_READWRITE = 0x04 : This is a standard memory protection used with VirtualAllocEx. It gives us Read and Write permissions in an assingned memory space but not execution.
VIRTUAL_MEM = Used with VirtualAllocEx to reserve an address range and commit physical memory in a single call. 0x1000 represents MEM_COMMIT and 0x2000 represents MEM_RESERVE.
              When used with | (bitwise OR) it results in hexadecimal 0x3000 which is MEM_COMMIT | MEM_RESERVE
PROCESS_ALL_ACCESS = Grants access rights! 
                     0x000F0000 being STANDARD_RIGHTS_REQUIRED like WO(write owner), WD(Write DACL), RC (Read Control) and DE (DELETE) of ACCESS_MASK(DWORD data type that defines standard, specific, and generic rights)
                     0x00100000 being SYNCHRONIZE which is used to Synchronize the ACCESS_MASK
                     0xFFF being PROCESS_ALL_ACCESS which grants All possible access rights for a process.
"""
PAGE_READWRITE = 0x04
VIRTUAL_MEM = (0x1000 | 0x2000)
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
kernel32 = ctypes.windll.kernel32

#get user input while also ensuring the PID is an int value
def get_user_int(prompt):
    global pid
    global ddl_path
    global dll_len
    while True:
        try:
            user_input = input(prompt)
            get_user_int = int(user_input)
            return get_user_int
        except ValueError:
            print("[!] Invalid input")

pid = get_user_int("[>] Please provide the Process PID you wish to inject to: ")
dll_pathinput = input("[>] Please provide the path to your DLL. Format Example(C:\\path\\to\\your.dll): ")
dll_path = bytes(dll_pathinput, 'utf-8')
dll_len = len(dll_path)+1

if pid is not None:
    print(f"[>] PID captured as {pid}")  
if dll_pathinput is not None:
    print(f"[>] Path to DLL captured as {dll_pathinput}")

#where the actual injection code is
def inject_dll(pid, dll_path):

#Open host process
    host_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, (pid))
    if not host_process:
        print(f"[!] Failed to open process {pid}")
        return False
#Allocate memory in the host process with the rights mentioned above for the Dll path        
    arg_address = kernel32.VirtualAllocEx(
        host_process, 
        0, 
        dll_len, 
        VIRTUAL_MEM, 
        PAGE_READWRITE
    )
#Write the Dll Path into allocated memory
    written = c_int(0)
    kernel32.WriteProcessMemory(
        host_process, 
        arg_address, 
        dll_path, 
        dll_len, 
        byref(written)
    )
#creating a remote thread to call to LoadLibrary in
    h_kernel32 = kernel32.GetModuleHandleA(b"kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, b"LoadLibraryA")

    thread_id = c_ulong(0)
    if not kernel32.CreateRemoteThread(
        host_process, 
        None, 
        0, 
        h_loadlib, 
        arg_address, 
        0, 
        byref(thread_id)
    ):
        print("[!] Failed to create remote thread")
        return False

    print(f"[+] DLL injected successfully into PID {pid}")
    return True
if __name__ == "__main__":
    if os.path.exists(dll_path):
        inject_dll(pid, dll_path)
    else:
        print("[!] DLL file not found")     

while True:
    exit_input = input("[>] Please Enter 'exit' to stop): ")
     
    if exit_input.lower() == "exit":
         print("[>] Exiting Program")
         break
         sys.exit(0)
    else:
         print("[>] Please enter 'exit' to stop")

if __name__ == "__main__":
    if os.path.exists(dll_path):
        inject_dll(pid, dll_path)
    else:
        print("[!] DLL file not found")     