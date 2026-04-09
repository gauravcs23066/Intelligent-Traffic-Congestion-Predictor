def bayes_theorem(p_rain, p_clouds_given_rain, p_clouds):
    print("\n--- Bayes Theorem Calculation ---\n")
    
    print(f"Step 1: P(Rain) = {p_rain}")
    
    print(f"Step 2: P(Clouds | Rain) = {p_clouds_given_rain}")
    
    print(f"Step 3: P(Clouds) = {p_clouds}")
    
    numerator = p_clouds_given_rain * p_rain
    print(f"\nStep 4: Numerator = P(Clouds | Rain) × P(Rain)")
    print(f"         = {p_clouds_given_rain} × {p_rain} = {numerator}")

    result = numerator / p_clouds
    print(f"\nStep 5: P(Rain | Clouds) = Numerator / P(Clouds)")
    print(f"         = {numerator} / {p_clouds} = {result}")
    
    return result

p_rain = 0.3
p_clouds_given_rain = 0.8
p_clouds = 0.5

final_result = bayes_theorem(p_rain, p_clouds_given_rain, p_clouds)

print("\nFinal Answer: Probability of Rain given Clouds =", final_result)