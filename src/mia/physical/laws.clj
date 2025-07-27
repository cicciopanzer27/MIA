(ns mia.physical.laws
  (:require [mia.symbolic.mathematics :as math]
            [mia.physical.constants :as const]))

;; === MECCANICA SIMBOLICA ===
(defn newton-second-law [mass acceleration]
  "F = ma simbolicamente"
  `(* ~mass ~acceleration))

(defn kinetic-energy [mass velocity]
  "KE = ½mv² simbolicamente"
  `(* 1/2 ~mass (^ ~velocity 2)))

;; === ELETTROMAGNETISMO SIMBOLICO ===
(defn coulomb-law [charge1 charge2 distance]
  "F = k*q1*q2/r²"
  `(/ (* 'k ~charge1 ~charge2) (^ ~distance 2)))

;; === RELATIVITÀ SIMBOLICA ===
(defn mass-energy-equivalence [mass]
  "E = mc²"
  `(* ~mass (^ 'c 2)))