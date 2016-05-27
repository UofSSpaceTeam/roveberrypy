#ifndef ARM2016_INVKIN
#define ARM2016_INVKIN


void CalculatePositions(double r, double z) {
    // Variables to be used in calculation
    double L1 = ORIGIN_ELBOW;
    double L2 = ELBOW_END;
    double L1_p2 = L1*L1;
    double L1_p3 = L1*L1*L1;
    double L1_p4 = L1*L1*L1*L1;
    double L2_p2 = L2*L2;
    double L2_p3 = L2*L2*L2;
    double x0 = ORIGIN_L1BASE;
    double H = ORIGIN_L1CONN;
    double phi_c = PHI_ELBOW_L1CONN;
    double S = ELBOW_L2CONN;
    // Calculate zenith angles
    double phi1 = acos((L1_p3 * z + L1 * z * (-L2_p2+r_p2+z_p2)+(r_p2+z_p2) *
    sqrt(-((L1_p2 * r_p2 * (L1_p4+(-L2_p2+r_p2+z_p2)*(-L2_p2+r_p2+z_p2)-2 * L1_p2 *
    (L2_p2+r_p2+z_p2)))/((r_p2+z_p2)*(r_p2+z_p2)))))/(2 * L1_p2 * (r_p2+z_p2)));
    double phi2 = acos(-1*((L1_p3 * z-L1 * z * (L2_p2+r_p2+z_p2)+(r_p2+z_p2) *
    sqrt(-1*((L1_p2 * r_p2 * (L1_p4+(-L2_p2+r_p2+z_p2)*(-L2_p2+r_p2+z_p2)-2 * L1_p2 *
    (L2_p2+r_p2+z_p2)))/((r_p2+z_p2)*(r_p2+z_p2)))))/(2 * L1 * L2 * (r_p2+z_p2))));
    // Calculate linear actuator distances and subtract body lengths
    double pos1 = x0*x0 + H*H - 2*x0*H*cos(PI/2+phi1-phi_c) - L1_BODY_LENGTH;
    double pos2 = L1_p2 + S*S - 2*L1*S*cos(phi1 + PI - phi2) - L2_BODY_LENGTH;
    // Convert to digital positions
    g_destination[3] = L1_PHYS_DIGI[0] * pos1 * 1000 + L1_PHYS_DIGI[1];
    g_destination[4] = L2_PHYS_DIGI[0] * pos2 * 1000 + L2_PHYS_DIGI[1];
}


#endif
