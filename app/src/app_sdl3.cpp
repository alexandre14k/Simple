// app/src/app_sdl3.cpp
#include "app_imgui.hpp"
#include "app_sdl3.hpp"
#include <SDL3/SDL.h>

void* app_sdl3_initialiser() {
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        return nullptr;
    }

    return reinterpret_cast<void*>(1);
}

void* app_sdl3_creer_fenetre(
    const char* titre,
    int largeur,
    int hauteur
) {
    SDL_Window* fenetre = SDL_CreateWindow(
        titre,
        largeur,
        hauteur,
        SDL_WINDOW_RESIZABLE
    );

    if (fenetre == nullptr) {
        return nullptr;
    }

    SDL_SetWindowMinimumSize(
        fenetre,
        largeur,
        hauteur
    );

    return fenetre;
}

void* app_sdl3_creer_rendu(void* fenetre) {
    return SDL_CreateRenderer(
        static_cast<SDL_Window*>(fenetre),
        nullptr
    );
}

void app_sdl3_demander_fermeture() {
    SDL_Event evenement{};

    evenement.type = SDL_EVENT_QUIT;
    SDL_PushEvent(&evenement);
}

void app_sdl3_detruire_rendu(void* rendu) {
    SDL_DestroyRenderer(
        static_cast<SDL_Renderer*>(rendu)
    );
}

void app_sdl3_detruire_fenetre(void* fenetre) {
    SDL_DestroyWindow(
        static_cast<SDL_Window*>(fenetre)
    );
}

bool app_sdl3_traiter_evenements(
    bool* enCours
) {
    SDL_Event evenement;

    while (SDL_PollEvent(&evenement)) {
        app_imgui_traiter_evenement(&evenement);

        if (evenement.type == SDL_EVENT_QUIT) {
            *enCours = false;
            return true;
        }
    }

    return false;
}

void app_sdl3_definir_couleur_rendu(
    void* rendu,
    unsigned char rouge,
    unsigned char vert,
    unsigned char bleu,
    unsigned char alpha
) {
    SDL_SetRenderDrawColor(
        static_cast<SDL_Renderer*>(rendu),
        rouge,
        vert,
        bleu,
        alpha
    );
}

void app_sdl3_effacer_rendu(void* rendu) {
    SDL_RenderClear(
        static_cast<SDL_Renderer*>(rendu)
    );
}

void app_sdl3_presenter_rendu(void* rendu) {
    SDL_RenderPresent(
        static_cast<SDL_Renderer*>(rendu)
    );
}

void app_sdl3_terminer() {
    SDL_Quit();
}