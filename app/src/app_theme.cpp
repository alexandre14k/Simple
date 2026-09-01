// app/src/app_theme.cpp
#include "app_theme.hpp"
#include <imgui.h>
#include <SDL3/SDL.h>
#include <cfloat>

static constexpr float app_theme_menu_minimum_largeur = 240.0f;
static constexpr float app_theme_menu_minimum_hauteur = 180.0f;
static constexpr float app_theme_largeur_reference = 1280.0f;
static constexpr float app_theme_hauteur_reference = 720.0f;
static constexpr float app_theme_taille_police = 18.0f;

void app_theme_appliquer() {
    ImGuiIO& io = ImGui::GetIO();

    io.IniFilename = nullptr;

    app_theme_appliquer_police();
    app_theme_appliquer_style();
    app_theme_definir_couleur_fond();
}

void app_theme_appliquer_echelle(
    void* fenetre
) {
    static constexpr float largeur_reference = 1280.0f;
    static constexpr float hauteur_reference = 720.0f;

    static constexpr float echelle_minimum = 0.75f;
    static constexpr float echelle_maximum = 2.0f;

    int largeur = 0;
    int hauteur = 0;

    SDL_GetWindowSize(
        static_cast<SDL_Window*>(fenetre),
        &largeur,
        &hauteur
    );

    float echelle_largeur =
        static_cast<float>(largeur)
        / largeur_reference;

    float echelle_hauteur =
        static_cast<float>(hauteur)
        / hauteur_reference;

    float echelle =
        echelle_largeur < echelle_hauteur
        ? echelle_largeur
        : echelle_hauteur;

    if (echelle < echelle_minimum) {
        echelle = echelle_minimum;
    }

    if (echelle > echelle_maximum) {
        echelle = echelle_maximum;
    }

    ImGui::GetIO().FontGlobalScale = echelle;
}

void app_theme_appliquer_taille_menu() {
    ImGui::SetNextWindowSizeConstraints(
        ImVec2(
            app_theme_menu_minimum_largeur,
            app_theme_menu_minimum_hauteur
        ),
        ImVec2(
            FLT_MAX,
            FLT_MAX
        )
    );
}

void app_theme_appliquer_police() {
    ImGuiIO& io = ImGui::GetIO();

    io.Fonts->Clear();

    ImFontConfig configuration{};

    configuration.SizePixels =
        app_theme_taille_police;

    io.Fonts->AddFontDefault(
        &configuration
    );
}

void app_theme_appliquer_style() {
    ImGui::StyleColorsLight();

    ImGuiStyle& style = ImGui::GetStyle();

    style.WindowRounding = 4.0f;
    style.FrameRounding = 4.0f;
    style.PopupRounding = 4.0f;
    style.ChildRounding = 4.0f;
    style.GrabRounding = 4.0f;
}

void app_theme_definir_couleur_fond() {
    ImGuiStyle& style = ImGui::GetStyle();

    style.Colors[ImGuiCol_WindowBg] =
        ImVec4(
            0.92f,
            0.92f,
            0.92f,
            1.0f
        );
}