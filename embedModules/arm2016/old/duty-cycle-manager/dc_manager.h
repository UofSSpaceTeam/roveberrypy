// Enumeration of Ramp-Function Stages
typedef enum {
    RAMP_UP,
    POSITION_SYNC,
    RAMP_DOWN,
    MIN_VEL,
    DONE
} ERFStage;

// Basic configuration
#define DCM_SIZE 8
#define MAX_DC 255.0

// Duty-cycle manager variables
static const float  TIME_RAMP_UP_MS   = 1000;     //  Time of ramp-up
static const float  DCM_PERIOD_MS     = 100;      //  Period of duty-cycle manager
static const float  DCM_MIN_VEL_INC   = MAX_DC * DCM_PERIOD_MS / TIME_RAMP_UP_MS;
static uint_t   DCM_ndone;
static uint_t   DCM_nmoves;              // number of movements to manage
static float    DCM_rd_dists[DCM_SIZE];  // ramp-down distances of movements
static float    DCM_min_vels[DCM_SIZE];  // minimum velocities for MIN_VELO stage of movements
static ERFStage DCM_stages  [DCM_SIZE];  // stages of movements

// Initialize the duty-cycle manager
// @param nmoves The number of movements which will be made
// @param dists Array of the normalized distances of the moves
// @param rd_dists Array of the normalized distances to begin ramp-down
// @param min_vels Array of the normalized minimum velocities for each movement
void DCManager_init(uint_t nmoves, float* rd_dists, float* min_vels)
{
    // Basic setup
    DCM_nmoves  = nmoves;
    DCM_ndone   = 0;
    if(nmoves == 0) return;
    // Copy the given parameters to the duty-cycle managers variables
    for(uint_t i = 0; i < DCM_nmoves; ++i) {
        DCM_rd_dists[i] = rd_dists[i];
        DCM_min_vels[i] = min_vels[i];
        if(dists > 0) {
            DCM_stages[i] = RAMP_UP;
        } else {
            DCM_stages[i] = DONE;
            ++DCM_ndone;
        }
    }
}

// Update the duty-cycle for each movement.
// @param elapsed_ms Elapsed time in milliseconds since movements began.
// @param dists Normalized distances remaining in each movement.
// @param vels Normalized velocities of each movement.
// @param dc Duty-cycle of each movement. On exit it is update with what the new
//           recomended duty-cycles.
// @return Whether or not all movements are done.
int DCManager_update(float elapsed_ms, float* dists, float* vels, int* dc)
{
    // Find the max distance remaining
    float max_dist = dists[0];
    for(uint_t i = 0; i < DCM_nmoves; ++i) {
        if(dists[i] > max_dist) max_dist = dists[i];
    }
    // Loop through each movement
    for(uint_t i = 0; i < DCM_nmoves; ++i) {
        // Check movement didn't finish unnoticed
        if(DCM_stages[i] != DONE && dists[i] <= 0) {
            DCM_stages[i] = DONE;
            ++DCM_ndone;
        }
        // Calculate the duty-cycle scale for this movement
        float scale = MAX_DC * ((float) dists[i]) / ((float) max_dist);
        // Assign duty-cycle based on ramp-function stage
        switch(DCM_stages[i]) {
        // Ramp-up the duty-cycle for this movement
        case RAMP_UP:
            float t =  elapsed_ms / TIME_RAMP_UP_MS;
            if (elapsed_ms > TIME_RAMP_UP_MS) {
                DCM_stages[i] = POSITION_SYNC;
            } else if(dists[i] < DCM_rd_dists[i]) {
                DCM_stages[i] = RAMP_DOWN;
            } else {
                dc[i] = scale * t * t (3.0 - 2.0 * t);
            }
            break;
        // Syncronize the relative position of this movement with the others
        case POSITION_SYNC:
            if(dists[i] < DCM_rd_dists[i]) {
                DCM_stages[i] = RAMP_DOWN;
            } else {
                dc[i] = scale;
            }
            break;
        // Ramp-down the duty-cycle until we're near the minimum velocity
        case RAMP_DOWN:
            // If we're within 10% of the minimum velocity then increment stage
            if(vels[i] <= 1.2 * DCM_min_vels[i]) {
                DCM_stages[i] = MIN_VEL;
            } else {
                float d = dists[i] / DCM_rd_dists[i];
                dc[i] = scale * (1.0 + 2.0 * d * d * d - 3.0 * d * d);
            }
            break;
        // Once near the minimum velocity, hold it until we reach the destination
        case MIN_VELO:
            if(dists[i] <= 0) {
                dc[i] = 0;
                DCM_stages[i] = DONE;
                ++DCM_ndone;
            } else if(vels[i] < DCM_min_vels[i]) {
                dc[i] = dc[i] + DCM_MIN_VEL_INC * (DCM_min_vels[i] - vels[i]);
            }
            break;
        // If we're done then make sure the duty-cycle is 0
        case DONE:
            dc[i] = 0;
            break;
        }
    }
    return DCM_ndone == DCM_nmoves;
}
