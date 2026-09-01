// app/src/gui.hpp
#pragma once

class Journal;
class PageMenu;
class PageNew;
class PageLoad;
class PageSettings;
enum class PageId : unsigned int;

class InterfaceGraphique {
public:
    InterfaceGraphique();
    ~InterfaceGraphique();
    int executer();

private:
    bool initialiser();
    void nettoyer();
    void bouclePrincipale();
    void traiterEvenements(
        bool* enCours
    );
    void dessinerImage();
    void dessinerPageActive();
    void changerPage(
        PageId identifiant
    );

    static void rappelPageStatique(
        void* contexte,
        unsigned int identifiant
    );

    void* fenetre;
    void* rendu;
    void* contexteImgui;
    bool estInitialise;

    Journal* journal;
    PageMenu* pageMenu;
    PageNew* pageNew;
    PageLoad* pageLoad;
    PageSettings* pageSettings;

    PageId pageActive;
};