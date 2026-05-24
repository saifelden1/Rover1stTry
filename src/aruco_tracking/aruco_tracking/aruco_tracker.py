import numpy as np
import cv2

class ArucoTracker:
    def __init__(self, arucoDictType: int = cv2.aruco.DICT_5X5_100):
        self.arucoDict = cv2.aruco.getPredefinedDictionary(arucoDictType)
        
        # Compatibility Check for OpenCV Versions
        if hasattr(cv2.aruco, 'DetectorParameters_create'):
            self.arucoParams = cv2.aruco.DetectorParameters_create()
        else:
            self.arucoParams = cv2.aruco.DetectorParameters()

        self.use_new_api = hasattr(cv2.aruco, "ArucoDetector")
        if self.use_new_api:
            self.arucoDetector = cv2.aruco.ArucoDetector(self.arucoDict, self.arucoParams)

    def detectMarkers(self, image: np.ndarray):
        if self.use_new_api:
            return self.arucoDetector.detectMarkers(image)
        else:
            return cv2.aruco.detectMarkers(image, self.arucoDict, parameters=self.arucoParams)

    def estimatePose(self, corners, markerSize, cameraMatrix, distCoeffs):
        if not corners:
            return np.array([]), np.array([])
        rvecs, tvecs = [], []
        objPoints = np.array([
            [-markerSize/2, markerSize/2, 0], [markerSize/2, markerSize/2, 0],
            [markerSize/2, -markerSize/2, 0], [-markerSize/2, -markerSize/2, 0]
        ], dtype=np.float32)

        for corner in corners:
            try:
                success, rvec, tvec = cv2.solvePnP(
                    objPoints, corner.reshape(-1, 2).astype(np.float32), 
                    cameraMatrix, distCoeffs, flags=cv2.SOLVEPNP_IPPE_SQUARE
                )
                if success:
                    rvecs.append(rvec)
                    tvecs.append(tvec)
            except Exception as e:
                print(f"Error in pose estimation: {e}")
        return np.array(rvecs), np.array(tvecs)

    def drawMarkers(self, image, corners, ids, rvecs, tvecs, cameraMatrix, distCoeffs):
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(image, corners, ids)
            for i in range(len(ids)):
                cv2.drawFrameAxes(image, cameraMatrix, distCoeffs, rvecs[i], tvecs[i], 0.1)
        return image

    def drawRejectedMarkers(self, image, rejected):
        cv2.aruco.drawDetectedMarkers(image, rejected, borderColor=(0, 0, 255))
        return image
