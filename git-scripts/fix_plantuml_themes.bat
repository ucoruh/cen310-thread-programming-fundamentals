@echo off
echo Fixing PlantUML theme issues...

REM Define the theme we want to use uniformly across all diagrams
set THEME_LINE=!theme cerulean

REM Fix common PlantUML diagrams
echo Fixing themes in common diagrams...
powershell -Command "(Get-Content ..\assets\thread_lifecycle.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\thread_lifecycle.puml"
powershell -Command "(Get-Content ..\assets\thread_communication.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\thread_communication.puml"
powershell -Command "(Get-Content ..\assets\synchronization_mechanisms.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\synchronization_mechanisms.puml"
powershell -Command "(Get-Content ..\assets\language_threading_comparison.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\language_threading_comparison.puml"
powershell -Command "if ((Get-Content ..\assets\threading_concepts_c4.puml) -match '!theme') { (Get-Content ..\assets\threading_concepts_c4.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\threading_concepts_c4.puml }"
powershell -Command "if ((Get-Content ..\assets\repository_structure.puml) -match '!theme') { (Get-Content ..\assets\repository_structure.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\repository_structure.puml }"
powershell -Command "if ((Get-Content ..\assets\learning_path.puml) -match '!theme') { (Get-Content ..\assets\learning_path.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\assets\learning_path.puml }"

REM Fix language-specific PlantUML diagrams
echo Fixing themes in language-specific diagrams...
powershell -Command "if (Test-Path ..\c-threads\assets\c_threading.puml) { (Get-Content ..\c-threads\assets\c_threading.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\c-threads\assets\c_threading.puml }"
powershell -Command "if (Test-Path ..\cpp-threads\assets\cpp_threading.puml) { (Get-Content ..\cpp-threads\assets\cpp_threading.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\cpp-threads\assets\cpp_threading.puml }"
powershell -Command "if (Test-Path ..\java-threads\assets\java_threading.puml) { (Get-Content ..\java-threads\assets\java_threading.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\java-threads\assets\java_threading.puml }"
powershell -Command "if (Test-Path ..\csharp-threads\assets\csharp_threading.puml) { (Get-Content ..\csharp-threads\assets\csharp_threading.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\csharp-threads\assets\csharp_threading.puml }"
powershell -Command "if (Test-Path ..\python-threads\assets\python_threading.puml) { (Get-Content ..\python-threads\assets\python_threading.puml) -replace '!theme.*', '%THEME_LINE%' | Set-Content ..\python-threads\assets\python_threading.puml }"

echo All PlantUML files have been updated to use the cerulean theme.
pause 