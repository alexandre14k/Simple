-- app/xmake.lua
target("app")
    add_files("main.cpp")
    add_files("src/*.cpp")
    add_includedirs("src")
    add_packages("libsdl3")
    add_deps("imgui")