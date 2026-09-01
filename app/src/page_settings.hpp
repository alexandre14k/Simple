// app/src/page_settings.hpp
#pragma once

typedef void (*RappelChangementPage)(
    void* contexte,
    unsigned int identifiant
);

class PageSettings {
public:
    void dessiner();
    void definirRappel(
        RappelChangementPage rappel,
        void* contexte
    );

private:
    RappelChangementPage rappelChangement = nullptr;
    void* contexteRappel = nullptr;
};