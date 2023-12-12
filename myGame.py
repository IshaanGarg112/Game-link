PlayerController.cs
using System.Collections;using System.Collections.Generic;using 
UnityEngine;[System.Serializable]public class Boundary{public float xMin,xMax,zMin,zMax;} 
public class PlayerController : MonoBehaviour
{public float speed;
public Rigidbody rb; 
public float tilt;
public GameObject shot;public Transform shotSpawn; 
public float fireRate;
private float nextFire;
public Boundary boundary;
public AudioSource audio; 
void Start()
{
audio = gameObject.GetComponent<AudioSource> ();
}
void Update()
{
if (Input.GetButton("Fire1") && Time.time > nextFire) { 
nextFire = Time.time + fireRate;
GameObject clone =
Instantiate(shot, shotSpawn.position, shotSpawn.rotation); 
audio.Play();
}
}
void FixedUpdate ()
{
float moveHorizontal = Input.GetAxis ("Horizontal"); 
float moveVertical = Input.GetAxis ("Vertical");
Vector3 movement = new Vector3 (moveHorizontal,0.0f,moveVertical); 
rb = GetComponent<Rigidbody> ();
rb.velocity = movement * speed;
transform.Translate (Input.acceleration.x, 0.0f,-Input.acceleration.z );rb.position = new 
Vector3
(
Mathf.Clamp(rb.position.x,boundary.xMin,boundary.xMax),0.0f, 
Mathf.Clamp(rb.position.z,boundary.zMin,boundary.zMax)
);
rb.rotation = Quaternion.Euler (0.0f,0.0f,rb.velocity.x * -tilt);
}
}
(b) GameController.cs
using System.Collections;
using System.Collections.Generic; 
using UnityEngine;
using UnityEngine. 
UI;
public class GameController : MonoBehaviour { 
public GameObject hazard;
public Vector3 spawnValues; 
public int hazardCount; 
public float spawnWait;
public float startWait; 
public float waveWait;
public Text scoreText;
ix
using System.Collections;
x
public Text gameOverText; 
private int score;
private bool gameOver; 
void Start () {
gameOver = false; 
gameOverText.text = ""; 
score = 0;
UpdateScore (); 
StartCoroutine(SpawnWaves ());
}
IEnumerator SpawnWaves ()
{
yield return new WaitForSeconds(startWait); 
while (true)
{
for (int i = 0; i < hazardCount; i++)
{
Vector3 spawnPosition = new Vector3 (Random.Range (-spawnValues.x, spawnValues.x), 
spawnValues.y, spawnValues.z);
Quaternion spawnRotation = Quaternion.identity; 
Instantiate (hazard, spawnPosition, spawnRotation);
yield return new WaitForSeconds (spawnWait);
}
yield return new WaitForSeconds (waveWait); 
if (gameOver){Application.LoadLevel ("menu"); 
break;
}
}
}
public void AddScore(int newScoreValue)
{
score += newScoreValue; 
UpdateScore ();
}
void UpdateScore()
{
scoreText.text = "Score:" + score;
}
public void GameOver()
{
gameOverText.text = "Game Over!"; 
gameOver = true;
}
}
(c) Mover.cs
using System.Collections;
using System.Collections.Generic; 
using UnityEngine;
public class Mover : MonoBehaviour { 
public Rigidbody rb;
public float speed;
void Start()
{
rb = GetComponent<Rigidbody> (); 
rb.velocity = transform.forward * speed;
}
}
(d) RandomRotator.cs
xi
using System.Collections.Generic; 
using UnityEngine;
public class RandomRotator : MonoBehaviour { 
public Rigidbody rb;
public float tumble; 
void Start ()
{
rb = GetComponent<Rigidbody> ();
rb.angularVelocity= Random.insideUnitSphere * tumble;
}
}
(e) DestroyByBoundary.cs
using System.Collections;
using System.Collections.Generic; 
using UnityEngine;
public class DestroyByBoundary : MonoBehaviour {
void OnTriggerExit(Collider other)
{
Destroy(other.gameObject);
}
}
(f)DestroyByContact.cs 
using System.Collections; 
using UnityEngine;
using UnityEngine.UI;
public class DestroyByContact : MonoBehaviour { 
public GameObject explosion;
public GameObject playerExplosion;
public int scoreValue;
private GameController gameController; 
void Start()
{
GameObject gameControllerObject = GameObject.FindWithTag ("GameController"); 
if (gameControllerObject != null)
{
gameController =gameControllerObject.GetComponent<GameController> ();
}
if (gameController == null)
{
Debug.Log("Cannot find 'GameController Script'");
}
}
void OnTriggerEnter(Collider other)
{
if (other.tag==("Boundary"))
{
return;
}
//Instantiate(explosion, transform.position, transform.rotation); 
Instantiate(playerExplosion, transform.position, transform.rotation); 
if (other.tag==("Player"))
{
Instantiate(playerExplosion, transform.position, transform.rotation); 
gameController.GameOver ();
}
(other.tag!=("Player")
)
{gameController.AddScore (scoreValue);
}
Destroy(other.gameObject); 
Destroy(gameObject);
}
}
(g) DestroyByTime.cs
using System.Collections;
using System.Collections.Generic; 
using UnityEngine;
public class DestroyByTime : MonoBehaviour {
public float lifetime; 
void Start ()
{
Destroy (gameObject,lifetime);
}
}