-- rig/xmake.lua
set_project("app")

set_targetdir("$(builddir)")

add_rules(
    "mode.debug",
    "mode.release"
)

if is_mode("release") then
    set_optimize("smallest")
    set_policy(
        "build.release.strip",
        true
    )
-- comment out these two settings below to enable dynamic build
--    set_runtimes("c++_static")
end

set_languages("c++20")

includes("../ext/xmake.lua")
includes("../app/xmake.lua")