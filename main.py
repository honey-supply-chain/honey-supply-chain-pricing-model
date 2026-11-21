from common.db import SessionLocal

from phqi.phqi_iteration_2 import PHQIIteration2
from phqi import PHQI

from si.ahp_user_service import AhpUserService
from si.evaluation_runner import EvaluationRunner
from si.repository.apiary_repository import ApiaryRepository
from si.repository.criterion_repository import CriterionRepository
from si.repository.normalization_parameter_repository import (
    NormalizationParameterRepository
)
from si.repository.pairwise_comparison_repository import (
    PairwiseComparisonRepository
)
from si.repository.sensor_data_repository import SensorDataRepository
from si.repository.user_repository import UserRepository
from si.repository.water_source_repository import WaterSourceRepository
from si.sensor_aggregation_service import SensorAggregationService

from mci import MCI
from qi import QI

from pricing.price_model_iteration_1 import PriceModel as PriceModelIteration1
from pricing.price_model_iteration_2 import PriceModel as PriceModelIteration2

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate_si(
    db,
    user_id: int,
    station: str,
    year: int,
    mac: str,
) -> float:
    """
    Calculates the Site Index (SI) using real sensor data
    and the AHP configuration stored in the database.
    """

    criterion_repo = CriterionRepository(db)
    comparison_repo = PairwiseComparisonRepository(db)
    normalization_repo = NormalizationParameterRepository(db)
    user_repo = UserRepository(db)
    sensor_data_repo = SensorDataRepository(db)
    apiary_repo = ApiaryRepository(db)
    water_source_repo = WaterSourceRepository(db)

    sensor_aggregation_service = SensorAggregationService(
        sensor_data_repo,
        water_source_repo
    )

    ahp_service = AhpUserService(
        criterion_repo,
        comparison_repo,
        normalization_repo
    )

    evaluation_runner = EvaluationRunner(
        sensor_aggregation_service,
        ahp_service,
        user_repo,
        apiary_repo,
        db
    )

    return evaluation_runner.evaluate_station(
        user_id,
        station,
        year,
        mac
    )


def calculate_phqi(
    water_content: float,
    hmf: float,
    invertase: float,
    naturally_enzyme_weak: bool,
) -> float:
    """
    Calculates PHQI using iteration 1.
    """

    phqi = PHQI()

    return phqi.calculate(
        water_content=water_content,
        hmf=hmf,
        invertase=invertase,
        naturally_enzyme_weak=naturally_enzyme_weak,
    )


def calculate_phqi_iteration_2(
    water_content: float,
    hmf: float,
    invertase: float,
    naturally_enzyme_weak: bool,
) -> float:
    """
    Calculates PHQI using iteration 2.
    """

    phqi = PHQIIteration2()

    return phqi.calculate(
        water_content=water_content,
        hmf=hmf,
        invertase=invertase,
        naturally_enzyme_weak=naturally_enzyme_weak,
    )


def calculate_mci(
    variety: str,
    origin: str,
    certification: str,
    award: str,
) -> float:
    """
    Calculates the Market Criteria Index (MCI).
    """

    mci = MCI()

    return mci.calculate(
        variety=variety,
        origin=origin,
        certification=certification,
        award=award,
    )


def calculate_qi(
    phqi_score: float,
    mci_score: float,
    si_score: float,
) -> float:
    """
    Calculates the aggregated Quality Index (QI).

    PHQI, MCI and SI are already normalized
    to the range 0-1.
    """

    qi = QI()

    return qi.calculate(
        phqi=phqi_score,
        mci=mci_score,
        si=si_score,
    )


def main():

    # =============================================
    # GENERAL CONFIGURATION
    # =============================================

    user_id = 1
    year = 2024
    base_price = 5.00
    floor_price = 4.80

    # =============================================
    # REAL BEEKEEPING SITES
    # =============================================

    real_sites = [
        {
            "name": "BS-1",
            "station": "Bienenstand_1",
            "mac": "0eddd296-1275-40e5-9b2a-ea9c34aa5b60",
        },
        {
            "name": "BS-3",
            "station": "Bienenstand_3",
            "mac": "a469fc22-1fa1-4bfc-aff8-89c936cb42fa",
        },
        {
            "name": "BS-5",
            "station": "Bienenstand_5",
            "mac": "c12be4c2-a807-404c-9b57-54d7ca1a63c9",
        },
    ]

    # =============================================
    # PRODUCT SCENARIOS
    # =============================================

    scenarios = [
        {
            "name": "Best-Case",

            "phqi": {
                "water_content": 15.8,
                "hmf": 4.5,
                "invertase": 50.0,
                "naturally_enzyme_weak": True,
            },

            "mci": {
                "variety": "fir honey",
                "origin": "regional gps verified",
                "certification": "bio austria",
                "award": "gold",
            },
        },

        {
            "name": "Standard",

            "phqi": {
                "water_content": 17.2,
                "hmf": 12.5,
                "invertase": 72.0,
                "naturally_enzyme_weak": False,
            },

            "mci": {
                "variety": "mixed blossom honey",
                "origin": "regional",
                "certification": "",
                "award": "",
            },
        },

        {
            "name": "Worst-Case",

            "phqi": {
                "water_content": 23.5,
                "hmf": 48.0,
                "invertase": 4.0,
                "naturally_enzyme_weak": False,
            },

            "mci": {
                "variety": "mixed blossom honey",
                "origin": "eu/non-eu mixture",
                "certification": "",
                "award": "",
            },
        },

        {
            "name": "Gatekeeper",

            "phqi": {
                "water_content": 21.5,
                "hmf": 48.0,
                "invertase": 4.0,
                "naturally_enzyme_weak": False,
            },

            "mci": {
                "variety": "fir honey",
                "origin": "regional gps verified",
                "certification": "bio austria",
                "award": "gold",
            },
        },
    ]

    # =============================================
    # DATABASE
    # =============================================

    db = SessionLocal()

    try:

        # =============================================
        # CALCULATE SI FOR REAL SITES
        # =============================================

        sites = []

        for site in real_sites:

            print(
                f"Calculating SI for {site['name']} "
                f"({site['station']})..."
            )

            si_score = calculate_si(
                db=db,
                user_id=user_id,
                station=site["station"],
                year=year,
                mac=site["mac"],
            )

            sites.append({
                "name": site["name"],
                "si": si_score,
            })

        # =============================================
        # ADD THEORETICAL EXTREMES
        # =============================================

        sites.append({
            "name": "Theoretical Minimum",
            "si": 0.00,
        })

        sites.append({
            "name": "Theoretical Maximum",
            "si": 1.00,
        })

        # =============================================
        # RESULT STORAGE
        # =============================================

        iteration_1_results = []
        iteration_2_results = []

        # =============================================
        # CALCULATE ALL SCENARIOS
        # =============================================

        for site in sites:

            for scenario in scenarios:

                phqi_data = scenario["phqi"]
                mci_data = scenario["mci"]

                # -------------------------------------
                # MCI
                # -------------------------------------

                mci_score = calculate_mci(
                    **mci_data
                )

                # =====================================
                # ITERATION 1
                # =====================================

                phqi_score_1 = calculate_phqi(
                    **phqi_data
                )

                qi_score_1 = calculate_qi(
                    phqi_score=phqi_score_1,
                    mci_score=mci_score,
                    si_score=site["si"],
                )

                multiplier_1 = PriceModelIteration1.calculate_multiplier(
                    qi_score_1
                )

                final_price_1 = PriceModelIteration1.calculate_price(
                    base_price=base_price,
                    qi=qi_score_1,
                )

                iteration_1_results.append({
                    "site": site["name"],
                    "si": site["si"],
                    "scenario": scenario["name"],
                    "phqi": phqi_score_1,
                    "mci": mci_score,
                    "qi": qi_score_1,
                    "multiplier": multiplier_1,
                    "price": final_price_1,
                })

                # =====================================
                # ITERATION 2
                # =====================================

                water_content = phqi_data["water_content"]

                if water_content > 23.0:

                    saleable = False
                    back_honey = False
                    phqi_score_2 = 0.0

                elif water_content > 20.0:

                    saleable = True
                    back_honey = True
                    phqi_score_2 = 0.0

                else:

                    saleable = True
                    back_honey = False

                    phqi_score_2 = calculate_phqi_iteration_2(
                        **phqi_data
                    )

                # -------------------------------------
                # NON-SALEABLE
                # -------------------------------------

                if not saleable:

                    iteration_2_results.append({
                        "site": site["name"],
                        "si": site["si"],
                        "scenario": scenario["name"],
                        "phqi": 0.0,
                        "mci": mci_score,
                        "qi": None,
                        "multiplier": None,
                        "price": None,
                        "saleable": False,
                        "back_honey": False,
                    })

                    continue

                # -------------------------------------
                # QI
                # -------------------------------------

                qi_score_2 = calculate_qi(
                    phqi_score=phqi_score_2,
                    mci_score=mci_score,
                    si_score=site["si"],
                )

                # -------------------------------------
                # PRICE
                # -------------------------------------

                multiplier_2 = PriceModelIteration2.calculate_multiplier(
                    qi_score_2
                )

                final_price_2 = PriceModelIteration2.calculate_price(
                    floor_price=floor_price,
                    qi=qi_score_2,
                )

                # -------------------------------------
                # STORE RESULT
                # -------------------------------------

                iteration_2_results.append({
                    "site": site["name"],
                    "si": site["si"],
                    "scenario": scenario["name"],
                    "phqi": phqi_score_2,
                    "mci": mci_score,
                    "qi": qi_score_2,
                    "multiplier": multiplier_2,
                    "price": final_price_2,
                    "saleable": True,
                    "back_honey": back_honey,
                })

        # =============================================
        # DISPLAY ITERATION 1
        # =============================================

        print()
        print("=" * 110)
        print("ITERATION 1")
        print("=" * 110)

        print(
            f"{'Site':<25}"
            f"{'SI':>8}"
            f"{'Scenario':<18}"
            f"{'PHQI':>8}"
            f"{'MCI':>8}"
            f"{'QI':>8}"
            f"{'Price':>12}"
        )

        print("-" * 110)

        for result in iteration_1_results:

            print(
                f"{result['site']:<25}"
                f"{result['si']:>8.3f}"
                f"{result['scenario']:<18}"
                f"{result['phqi']:>8.3f}"
                f"{result['mci']:>8.3f}"
                f"{result['qi']:>8.3f}"
                f"{result['price']:>10.2f} EUR"
            )

        # =============================================
        # DISPLAY ITERATION 2
        # =============================================

        print()
        print("=" * 110)
        print("ITERATION 2")
        print("=" * 110)

        print(
            f"{'Site':<25}"
            f"{'SI':>8}"
            f"{'Scenario':<18}"
            f"{'PHQI':>8}"
            f"{'MCI':>8}"
            f"{'QI':>8}"
            f"{'Price':>12}"
            f"{'Status':>15}"
        )

        print("-" * 110)

        for result in iteration_2_results:

            if not result["saleable"]:
                status = "NOT SALEABLE"
            elif result["back_honey"]:
                status = "BACK HONEY"
            else:
                status = "SALEABLE"

            print(
                f"{result['site']:<25}"
                f"{result['si']:>8.3f}"
                f"{result['scenario']:<18}"
                f"{result['phqi']:>8.3f}"
                f"{result['mci']:>8.3f}"
                f"{result['qi'] if result['qi'] is not None else 0.0:>8.3f}"
                f"{result['price'] if result['price'] is not None else 0.0:>10.2f} EUR"
                f"{status:>15}"
            )

        print("=" * 110)

        # =============================================
        # RESULT COUNT
        # =============================================

        print()
        print(
            f"Iteration 1 combinations: "
            f"{len(iteration_1_results)}"
        )

        print(
            f"Iteration 2 combinations: "
            f"{len(iteration_2_results)}"
        )

        # =============================================
        # CREATE DATAFRAME FOR COMPARISON
        # =============================================

        df_iteration_1 = pd.DataFrame(iteration_1_results)
        df_iteration_1["iteration"] = "Iteration 1"

        df_iteration_2 = pd.DataFrame(iteration_2_results)
        df_iteration_2["iteration"] = "Iteration 2"

        comparison_df = pd.concat(
            [df_iteration_1, df_iteration_2],
            ignore_index=True
        )

        print()
        print("=" * 110)
        print("COMBINED RESULTS")
        print("=" * 110)

        print(comparison_df.to_string(index=False))

        # =============================================
        # CREATE CHART
        # =============================================

        print()
        print("Results stored in:")
        print("  iteration_1_results")
        print("  iteration_2_results")

        create_price_comparison_chart(
            iteration_1_results,
            iteration_2_results
        )

    finally:
        db.close()


def create_price_comparison_chart(
    iteration_1_results,
    iteration_2_results,
    output_path="preismodell_vergleich.png"
):
    """
    Creates a comparison chart for price model iteration 1 and iteration 2.

    The results contain multiple sites and scenarios.
    Each site/scenario combination is compared between
    Iteration 1 and Iteration 2.
    """

    scenarios = [
        "Best-Case",
        "Standard",
        "Worst-Case",
        "Gatekeeper"
    ]

    sites = [
        "BS-1",
        "BS-3",
        "BS-5",
        "Theoretical Minimum",
        "Theoretical Maximum"
    ]

    # ---------------------------------------------------------
    # Ergebnisse nach Site + Scenario indexieren
    # ---------------------------------------------------------

    iteration_1_lookup = {
        (result["site"], result["scenario"]): result["price"]
        for result in iteration_1_results
    }

    iteration_2_lookup = {
        (result["site"], result["scenario"]): result["price"]
        for result in iteration_2_results
    }

    # ---------------------------------------------------------
    # Diagramm
    # ---------------------------------------------------------

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(14, 7.5),
        sharey=True
    )

    axes = axes.flatten()

    x = np.arange(len(scenarios))
    width = 0.36

    # ---------------------------------------------------------
    # Gemeinsame dynamische Y-Achse bestimmen
    # ---------------------------------------------------------

    all_prices = [
        result["price"]
        for result in iteration_1_results + iteration_2_results
        if result["price"] is not None
    ]

    max_price = max(all_prices)

    # Etwas zusätzlicher Platz oberhalb des höchsten Balkens
    y_max = max_price + 0.8

    # ---------------------------------------------------------
    # Diagramme erzeugen
    # ---------------------------------------------------------

    for index, site in enumerate(sites):

        ax = axes[index]

        # -----------------------------------------------------
        # Preise
        # -----------------------------------------------------

        prices_iteration_1 = [
            iteration_1_lookup.get(
                (site, scenario)
            )
            for scenario in scenarios
        ]

        prices_iteration_2 = [
            iteration_2_lookup.get(
                (site, scenario)
            )
            for scenario in scenarios
        ]

        # -----------------------------------------------------
        # Iteration 1
        # -----------------------------------------------------

        iteration_1_plot_values = [
            value if value is not None else 0
            for value in prices_iteration_1
        ]

        bars_iteration_1 = ax.bar(
            x - width / 2,
            iteration_1_plot_values,
            width,
            label="Iteration 1"
        )

        # -----------------------------------------------------
        # Iteration 2
        # -----------------------------------------------------

        iteration_2_plot_values = [
            value if value is not None else 0
            for value in prices_iteration_2
        ]

        bars_iteration_2 = ax.bar(
            x + width / 2,
            iteration_2_plot_values,
            width,
            label="Iteration 2"
        )

        # -----------------------------------------------------
        # Preise Iteration 1
        # -----------------------------------------------------

        for bar, value in zip(
            bars_iteration_1,
            prices_iteration_1
        ):

            if value is not None:

                if value >= 3.0:

                    # Preis innerhalb des Balkens
                    y_position = value * 0.80

                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        y_position,
                        f"{value:.2f} €",
                        ha="center",
                        va="top",
                        fontsize=11,
                        rotation=90,
                        bbox=dict(
                            facecolor="white",
                            edgecolor="none",
                            pad=1.5
                        )
                    )

                else:

                    # Preis oberhalb des kleinen Balkens
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        value + 0.12,
                        f"{value:.2f} €",
                        ha="center",
                        va="bottom",
                        fontsize=11,
                        rotation=90
                    )

        # -----------------------------------------------------
        # Preise / Status Iteration 2
        # -----------------------------------------------------

        for bar, value, scenario in zip(
            bars_iteration_2,
            prices_iteration_2,
            scenarios
        ):

            if value is None:

                annotation = "Nicht verkaufsfähig"

                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    0.25,
                    annotation,
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    rotation=90
                )

            else:

                if value >= 3.0:

                    # Preis innerhalb des Balkens
                    y_position = value * 0.80

                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        y_position,
                        f"{value:.2f} €",
                        ha="center",
                        va="top",
                        fontsize=11,
                        rotation=90,
                        bbox=dict(
                            facecolor="white",
                            edgecolor="none",
                            pad=1.5
                        )
                    )

                else:

                    # Preis oberhalb des kleinen Balkens
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        value + 0.12,
                        f"{value:.2f} €",
                        ha="center",
                        va="bottom",
                        fontsize=11,
                        rotation=90
                    )

        # -----------------------------------------------------
        # Achsen
        # -----------------------------------------------------

        ax.set_title(
            site,
            fontsize=12
        )

        ax.set_xticks(x)

        ax.set_xticklabels(
            scenarios,
            rotation=15,
            fontsize=10
        )

        # Gemeinsame dynamische Y-Achse
        ax.set_ylim(
            0,
            y_max
        )

        ax.grid(
            axis="y",
            alpha=0.25
        )

    # ---------------------------------------------------------
    # Sechstes Subplot als Legendenbereich verwenden
    # ---------------------------------------------------------

    legend_ax = axes[-1]

    legend_ax.axis("off")

    handles, labels = axes[0].get_legend_handles_labels()

    legend_ax.legend(
        handles,
        labels,
        loc="center",
        fontsize=11,
        frameon=False
    )

    # ---------------------------------------------------------
    # Y-Achsenbeschriftung
    # ---------------------------------------------------------

    fig.supylabel(
        "Modellierter Verkaufspreis (€ / 500-g-Glas)",
        fontsize=11
    )

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------

    fig.tight_layout(
        rect=[0.04, 0.03, 1, 0.98],
        h_pad=1.0,
        w_pad=1.0
    )

    # ---------------------------------------------------------
    # Speichern
    # ---------------------------------------------------------

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":
    main()