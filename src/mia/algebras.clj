(ns mia.algebras
  (:require [mia.core :as core]))

;; === ALGEBRA DI COMPOSIZIONE (SEMPLIFICATA) ===
(defn compose-atoms [atoms]
  "Compone atomi in una molecola (versione semplificata)"
  (let [elements (frequencies (map :element atoms))
        formula (cond
                  (= elements {:hydrogen 2 :oxygen 1}) "H2O"
                  (= elements {:carbon 1 :hydrogen 4}) "CH4"
                  :else "UNKNOWN")]
    (when (not= formula "UNKNOWN")
      (let [bonds []] ; Semplificato, non creiamo legami per ora
        (core/create-molecule atoms bonds formula)))))

;; Altre funzioni algebriche che potremo usare in futuro
(defn field-effect [source target]
  "Calcola l'effetto di campo tra due entità"
  (let [source-charge (if (= (:element source) :hydrogen) 1
                         (- (:protons source) (:electrons source)))
        target-charge (if (= (:element target) :hydrogen) 1
                         (- (:protons target) (:electrons target)))]
    (cond
      (and (pos? source-charge) (neg? target-charge)) :attractive
      (and (neg? source-charge) (pos? target-charge)) :attractive
      :else :neutral)))