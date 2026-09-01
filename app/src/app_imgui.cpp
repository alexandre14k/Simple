// app/src/app_imgui.cpp
#include "app_imgui.hpp"
#include "app_theme.hpp"
#include <imgui.h>
#include <imgui_impl_sdl3.h>
#include <imgui_impl_sdlrenderer3.h>
#include <SDL3/SDL.h>

void* app_imgui_creer_contexte() {
    IMGUI_CHECKVERSION();

    return ImGui::CreateContext();
}

void app_imgui_detruire_contexte(void* contexte) {
    ImGui::DestroyContext(
        static_cast<ImGuiContext*>(contexte)
    );
}

void app_imgui_initialiser_sdl3(
    void* fenetre,
    void* rendu
) {
    ImGui_ImplSDL3_InitForSDLRenderer(
        static_cast<SDL_Window*>(fenetre),
        static_cast<SDL_Renderer*>(rendu)
    );

    ImGui_ImplSDLRenderer3_Init(
        static_cast<SDL_Renderer*>(rendu)
    );
}

void app_imgui_configurer() {
    app_theme_appliquer();
}

void app_imgui_terminer_sdl3() {
    ImGui_ImplSDLRenderer3_Shutdown();
    ImGui_ImplSDL3_Shutdown();
}

void app_imgui_nouvelle_image() {
    ImGui_ImplSDLRenderer3_NewFrame();
    ImGui_ImplSDL3_NewFrame();
}

void app_imgui_nouvelle_frame() {
    ImGui::NewFrame();
}

bool app_imgui_commencer(
    const char* titre
) {
    return ImGui::Begin(
        titre,
        nullptr,
        ImGuiWindowFlags_NoResize
    );
}

void app_imgui_terminer() {
    ImGui::End();
}

void app_imgui_rendre() {
    ImGui::Render();
}

void app_imgui_rendre_donnees(
    void* rendu
) {
    ImGui_ImplSDLRenderer3_RenderDrawData(
        ImGui::GetDrawData(),
        static_cast<SDL_Renderer*>(rendu)
    );
}

void app_imgui_traiter_evenement(
    void* evenement
) {
    ImGui_ImplSDL3_ProcessEvent(
        static_cast<SDL_Event*>(evenement)
    );
}

void app_imgui_texte(
    const char* texte
) {
    ImGui::Text(
        "%s",
        texte
    );
}

bool app_imgui_bouton(
    const char* texte
) {
    static constexpr float espacement = 8.0f;

    ImVec2 taille(
        -1.0f,
        ImGui::GetFrameHeight()
    );

    bool resultat = ImGui::Button(
        texte,
        taille
    );

    ImGui::Dummy(
        ImVec2(
            0.0f,
            espacement
        )
    );

    return resultat;
}

void app_imgui_preparer_fenetre_menu() {
    ImVec2 taille =
        ImGui::GetIO().DisplaySize;

    float largeur =
        taille.x - 32.0f;

    float hauteur =
        taille.y - 32.0f;

    if (largeur < 1.0f) {
        largeur = 1.0f;
    }

    if (hauteur < 1.0f) {
        hauteur = 1.0f;
    }

    ImGui::SetNextWindowPos(
        ImVec2(
            16.0f,
            16.0f
        ),
        ImGuiCond_Always
    );

    ImGui::SetNextWindowSize(
        ImVec2(
            largeur,
            hauteur
        ),
        ImGuiCond_Always
    );
}

void app_imgui_texte_gras(
    const char* texte
) {
    ImVec2 position =
        ImGui::GetCursorScreenPos();

    ImGui::SetCursorScreenPos(
        ImVec2(
            position.x + 1.0f,
            position.y
        )
    );

    ImGui::Text(
        "%s",
        texte
    );

    ImGui::SetCursorScreenPos(
        position
    );

    ImGui::Text(
        "%s",
        texte
    );
}

void app_imgui_centrer_groupe_menu(
    unsigned int nombre_elements
) {
    float hauteur_element =
        ImGui::GetFrameHeight();

    float espacement =
        8.0f;

    float hauteur_totale =
        (
            hauteur_element
            * static_cast<float>(
                nombre_elements
            )
        )
        + (
            espacement
            * static_cast<float>(
                nombre_elements - 1
            )
        );

    float hauteur_disponible =
        ImGui::GetContentRegionAvail().y;

    float position =
        (hauteur_disponible - hauteur_totale)
        * 0.5f;

    if (position < 0.0f) {
        position = 0.0f;
    }

    ImGui::SetCursorPosY(
        ImGui::GetCursorPosY()
        + position
    );
}