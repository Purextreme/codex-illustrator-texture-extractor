Option Explicit

If WScript.Arguments.Count < 1 Or WScript.Arguments.Count > 2 Then
  WScript.Echo "Usage: cscript //nologo illustrator_com_runner.vbs <script.jsx> [Illustrator.ProgID]"
  WScript.Quit 2
End If

Dim illustratorApp, jsxPath, progId
jsxPath = WScript.Arguments(0)
progId = "Illustrator.Application.28"
If WScript.Arguments.Count = 2 Then progId = WScript.Arguments(1)

On Error Resume Next
Set illustratorApp = GetObject(, progId)
If Err.Number <> 0 Then
  Err.Clear
  Set illustratorApp = CreateObject(progId)
  If Err.Number <> 0 Then
    WScript.Echo "COM_CONNECT_ERROR " & Err.Number & " " & Err.Description
    WScript.Quit 3
  End If
End If

Err.Clear
illustratorApp.DoJavaScriptFile jsxPath
If Err.Number <> 0 Then
  WScript.Echo "JSX_ERROR " & Err.Number & " " & Err.Description
  WScript.Quit 4
End If

WScript.Echo "COM_OK"
WScript.Quit 0
