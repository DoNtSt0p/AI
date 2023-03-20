g++ -c main.cpp -o build_file.o -I C:/A/SFML_MinGW64/include -D SFML_STATIC
g++ build_file.o -o run.exe -L C:/A/SFML_MinGW64/lib -l sfml-graphics-s -l sfml-window-s -l sfml-system-s -l winmm -l gdi32 -l opengl32 -l freetype -static-libgcc -static-libstdc++
run run.exe