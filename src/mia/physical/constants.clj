(ns mia.physical.constants
  (:require [mia.symbolic.mathematics :as math]))

;; === COSTANTI FISICHE FONDAMENTALI ===
(def fundamental-constants
  {:speed-of-light
   {:symbol 'c
    :value 299792458 :units "m/s"
    :definition "speed of electromagnetic radiation in vacuum"
    :invariance :lorentz-invariant
    :ontological-status :spacetime-geometry}

   :planck-constant
   {:symbol 'ℏ
    :value 1.054571817e-34 :units "J⋅s"
    :definition "quantum of action"
    :invariance :universal
    :ontological-status :quantum-discreteness}

   :gravitational-constant
   {:symbol 'G
    :value 6.67430e-11 :units "m³/kg⋅s²"
    :definition "strength of gravitational interaction"
    :invariance :universal
    :ontological-status :spacetime-curvature}})