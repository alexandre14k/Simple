-- ext/xmake.lua
add_requires(
    "libsdl3",
    {
        configs = {
            shared = true,
            x11_shared = true,
            wayland_shared = true
        }
    }
)

target("imgui")
    set_kind("shared")
    set_targetdir("../out/lib/imgui")
    add_files("repo/imgui/*.cpp")
    add_files("repo/imgui/backends/imgui_impl_sdl3.cpp")
    add_files("repo/imgui/backends/imgui_impl_sdlrenderer3.cpp")
    add_includedirs("repo/imgui", {public = true})
    add_includedirs("repo/imgui/backends", {public = true})
    add_packages("libsdl3", {public = true})