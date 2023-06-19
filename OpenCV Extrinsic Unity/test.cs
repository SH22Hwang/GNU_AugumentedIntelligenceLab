using UnityEngine;

public class MarkerController : MonoBehaviour
{
    public int markerId; // The ID of the marker
    public Vector3 positionOffset; // Offset position for marker

    private Vector3 initialPosition;
    private Quaternion initialRotation;

    // Function to update the marker position and rotation
    public void UpdateMarkerPose(Vector3 translationVector, Vector3 rotationVector)
    {
        // Apply offset to the translation vector
        translationVector += positionOffset;

        // Convert rotation vector to quaternion
        Quaternion rotation = Quaternion.Euler(rotationVector);

        // Update marker's position and rotation
        transform.position = initialPosition + translationVector;
        transform.rotation = initialRotation * rotation;
    }

    private void Start()
    {
        // Store initial position and rotation
        initialPosition = transform.position;
        initialRotation = transform.rotation;
    }
}
