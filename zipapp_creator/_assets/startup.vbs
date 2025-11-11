Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' get Python from environment variable
pythonExe = "${PYTHON_EXE}"
zipappFile = "${ZIPAPP_FILE}"

' check if zipappFile exists
If Not fso.FileExists(zipappFile) Then
    MsgBox "Zipapp file not found: " & zipappFile, vbCritical
    WScript.Quit
End If

' Try to run the zipapp file with Python
On Error Resume Next
WshShell.Run pythonExe & " """ & zipappFile & """", 0, False
If Err.Number <> 0 Then
    MsgBox "Unable to run zipapp! Please make sure Python is installed and added to PATH.", vbCritical
End If
On Error Goto 0

Set fso = Nothing
Set WshShell = Nothing