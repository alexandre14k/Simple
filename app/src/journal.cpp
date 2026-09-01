// app/src/journal.cpp
#include "journal.hpp"
#include <chrono>
#include <cstdio>
#include <ctime>
#include <fstream>

void Journal::formaterHorodatage(
    char* tampon,
    unsigned int taille
) {
    auto maintenant =
        std::chrono::system_clock::now();

    auto tempsC =
        std::chrono::system_clock::to_time_t(
            maintenant
        );

    auto epoque =
        maintenant.time_since_epoch();

    auto millisecondes =
        std::chrono::duration_cast<
            std::chrono::milliseconds
        >(epoque) % 1000;

    std::tm decompose{};

#if defined(_WIN32)
    localtime_s(&decompose, &tempsC);
#else
    localtime_r(&tempsC, &decompose);
#endif

    std::snprintf(
        tampon,
        taille,
        "%04d%02d%02d-%02d%02d%02d.%03d",
        decompose.tm_year + 1900,
        decompose.tm_mon + 1,
        decompose.tm_mday,
        decompose.tm_hour,
        decompose.tm_min,
        decompose.tm_sec,
        static_cast<int>(
            millisecondes.count()
        )
    );
}

void Journal::consigner(
    const char* message
) {
    if (!journal_actif) {
        return;
    }

    retenir(message);
}

void Journal::retenir(
    const char* message
) {
    char horodatage[32];

    formaterHorodatage(
        horodatage,
        sizeof(horodatage)
    );

    std::ofstream fichier(
        "journal.log",
        std::ios::app
    );

    if (fichier.is_open()) {
        fichier
            << horodatage
            << " -- "
            << message
            << "\n";
    }
}