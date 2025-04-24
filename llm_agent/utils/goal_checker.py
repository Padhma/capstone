def goal_checker(elements, constraints):
    result = {}
    found = {}

    for key, expected in constraints.items():
        expected = str(expected).strip().lower()

        for el in elements:
            el_id = str(el.get("id", "")).strip().lower()
            el_text = str(el.get("text", "")).strip().lower()

            # Dynamic attribute checking
            if key == "brand" and "brand:" in el_text:
                brand_value = expected
                if brand_value in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "price" and "product-price" in el_id:
                price_str = el.get("text", "").replace("$", "").replace(",", "").strip()
                try:
                    price_val = float(price_str)
                    threshold = float(expected.replace("under", "").replace("$", "").strip())
                    result[key] = price_val < threshold
                    found[key] = price_val
                    break
                except ValueError:
                    result[key] = False
                    found[key] = "invalid"
                    break

            elif key == "screen" and "screen:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "ram" and "ram:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "ssd" and "ssd:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "cpu" and "cpu:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "gpu" and "gpu:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "battery" and "battery:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

            elif key == "weight" and "weight:" in el_text:
                if expected in el_text:
                    result[key] = True
                    found[key] = el_text
                    break

    # Check if all constraints are satisfied
    all_constraints_met = all(result.get(key, False) for key in constraints)
    if all_constraints_met:
        print(f"✅ All constraints are satisfied.")
        return True, {key: found.get(key, "unknown") for key in constraints}
    else:
        return False, {}