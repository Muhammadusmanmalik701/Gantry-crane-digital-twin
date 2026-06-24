package GantryAssignment

  model Plant
    // Parameters (SI units - sab correct)
    parameter Real m = 0.2 "Mass of container (kg)";
    parameter Real M = 10 "Mass of trolley (kg)";
    parameter Real r = 1 "Rope length (m)";
    parameter Real dp = 0.5 "Pendulum damping";
    parameter Real dc = 2 "Cart damping";
    parameter Real g = 9.81 "Gravity (m/s²)";

    // Variables with initial conditions
    Real x(start=0, fixed=true) "Trolley position (m)";
    Real v(start=0, fixed=true) "Trolley velocity (m/s)";
    Real theta(start=0, fixed=true) "Pendulum angle (rad)";
    Real omega(start=0, fixed=true) "Pendulum angular velocity (rad/s)";
    Real u "Control force on trolley (N)";

  equation
    der(x) = v;
    der(theta) = omega;

    // === Exact ODEs from assignment (no change) ===
    der(v) = (r * (dc * v - m * (g * sin(theta) * cos(theta) + r * sin(theta) * omega^2) - u) 
              - dp * cos(theta) * omega) 
             / (-r * (M + m * sin(theta)^2));

    der(omega) = (dp * omega * (m + M) 
                  + m^2 * r^2 * sin(theta) * cos(theta) * omega^2 
                  + m * r * (g * sin(theta) * (m + M) + cos(theta) * (u - dc * v))) 
                 / (m * r^2 * (-M - m * sin(theta)^2));

    // ================== CASE 1: u = 0 (self-test) ==================
    // Pehle yeh line uncomment karo aur neeche wali comment kar do
    //u = 0;

    // ================== CASE 2: Impulse (task point 15) ==================
    // Jab u=0 wala test pass ho jaye tab yeh uncomment kar do
    u = if time < 0.5 then 1000 else 0;

  end Plant;

end GantryAssignment;
