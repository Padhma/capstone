def goal_checker(elements, constraints):
    result = {key: False for key in constraints}  # Initialize assuming constraints are not met
    found = {}

    for el in elements:
        el_text = str(el.get("text", "")).strip().lower()

        for key, expected in constraints.items():
            expected = str(expected).strip().lower()

            # Dynamic attribute checking
            if key == "brand" and "brand:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text

            elif key == "ram" and "ram:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text

            # Similar checks applied for other keys
            elif key == "price" and "product-price" in el_text:
                price_str = el.get("text", "").replace("$", "").replace(",", "").strip()
                try:
                    price_val = float(price_str)
                    threshold = float(expected.replace("under", "").replace("$", "").strip())
                    result[key] = price_val < threshold
                    found[key] = price_val
                except ValueError:
                    result[key] = False
                    found[key] = "invalid"

            elif key in ["screen", "ssd", "cpu", "gpu", "battery", "weight"] and f"{key}:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text

    # Check if all constraints are satisfied
    all_constraints_met = all(result.values())
    if all_constraints_met:
        print(f"✅ All constraints are satisfied.")
        return True, {key: found.get(key, "unknown") for key in constraints}
    else:
        print(f"❌ Some constraints failed: {result}")
        return False, {}