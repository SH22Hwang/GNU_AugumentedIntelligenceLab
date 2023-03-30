#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

// matching pairs

vector<Point3f> objectPoints; // 3d world coordinates

vector<Point2f> imagePoints; // 2d image coordinates

// camera parameters

double m[] = {fx, 0, cx, 0, fy, cy, 0, 0, 1}; // intrinsic parameters

Mat A(3, 3, CV_64FC1, m); // camera matrix

double d[] = {k1, k2, p1, p2}; // k1,k2: radial distortion, p1,p2: tangential distortion

Mat distCoeffs(4, 1, CV_64FC1, d);

// estimate camera pose

Mat rvec, tvec; // rotation & translation vectors

solvePnP(objectPoints, imagePoints, A, distCoeffs, rvec, tvec);

// extract rotation & translation matrix

Mat R;

Rodrigues(rvec, R);

Mat R_inv = R.inv();

Mat P = -R_inv * tvec;

double *p = (double *)P.data;

// camera position

printf("x=%lf, y=%lf, z=%lf", p[0], p[1], p[2]);