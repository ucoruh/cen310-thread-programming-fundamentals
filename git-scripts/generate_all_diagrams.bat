@echo off
echo Generating all PlantUML diagrams...

REM First, fix any theme issues
echo Fixing PlantUML themes...
call fix_plantuml_themes.bat

REM Check if PlantUML jar exists, if not, download it
if not exist ..\assets\plantuml.jar (
    echo PlantUML jar not found. Downloading...
    call download_plantuml.bat
)

set PLANTUML_JAR=..\assets\plantuml.jar

REM Generate common diagrams
echo Generating common diagrams...
java -jar %PLANTUML_JAR% ..\assets\thread_lifecycle.puml
java -jar %PLANTUML_JAR% ..\assets\thread_communication.puml
java -jar %PLANTUML_JAR% ..\assets\synchronization_mechanisms.puml
java -jar %PLANTUML_JAR% ..\assets\language_threading_comparison.puml
java -jar %PLANTUML_JAR% ..\assets\threading_concepts_c4.puml
java -jar %PLANTUML_JAR% ..\assets\repository_structure.puml
java -jar %PLANTUML_JAR% ..\assets\learning_path.puml

REM Generate language-specific diagrams
echo Generating language-specific diagrams...
java -jar %PLANTUML_JAR% ..\c-threads\assets\c_threading.puml
java -jar %PLANTUML_JAR% ..\cpp-threads\assets\cpp_threading.puml
java -jar %PLANTUML_JAR% ..\java-threads\assets\java_threading.puml
java -jar %PLANTUML_JAR% ..\csharp-threads\assets\csharp_threading.puml
java -jar %PLANTUML_JAR% ..\python-threads\assets\python_threading.puml

REM Rename diagram files to remove spaces
echo Renaming diagram files to remove spaces...
call rename_diagram_files.bat

echo All diagrams generated successfully!
echo Image files are saved in the same directory as their .puml files.
pause 