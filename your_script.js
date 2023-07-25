import * as THREE from "https://unpkg.com/three@0.145.0/build/three.module.js";
import { OrbitControls } from "https://unpkg.com/three@0.145.0/examples/jsm/controls/OrbitControls.js";

let scene, camera, renderer, controls;


init();
let objects = [];
const babylonData = await fetch("phys.babylon").then((res) => res.json());
const meshes = babylonData.meshes;

function createObject(mesh) {
    const position = mesh.position;
    const rotation = mesh.rotation;
    const scaling = mesh.scaling;

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);

    cube.position.x = position[0];
    cube.position.y = position[1];
    cube.position.z = position[2];

    cube.rotation.x = rotation[0];
    cube.rotation.y = rotation[1];
    cube.rotation.z = rotation[2];

    cube.scale.x = scaling[0];
    cube.scale.y = scaling[1];
    cube.scale.z = scaling[2];

    if (!mesh.animations) {
        return cube;
    }
    
    const animations = mesh.animations;
    const rotationAnimation = animations[0];
    const positionAnimation = animations[1];

    const rotationKeys = rotationAnimation.keys;
    const positionKeys = positionAnimation.keys;
    var currentFrame = 0;

    objects.push({ cube, rotationKeys, positionKeys, currentFrame });
    return cube;
}
for (let i = 0; i < meshes.length; i++) {
    const mesh = meshes[i];
    scene.add(createObject(mesh));
}

let currentFrame = 0;

animate();

function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 5;

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    controls = new OrbitControls(camera, renderer.domElement);
}

function animate() {
    requestAnimationFrame(animate);

    // objects

    for (let i = 0; i < objects.length; i++) {

        const object = objects[i];
        const cube = object.cube;
        const rotationKeys = object.rotationKeys;
        const positionKeys = object.positionKeys;
        const currentFrame = object.currentFrame;
        frames = positionKeys.length;

        if (currentFrame >= frames) {
            object.currentFrame = 0;
        }
        
        const positionFrame = positionKeys[currentFrame];
        const positionValues = positionFrame.values;
        cube.position.set(
            positionValues[0],
            positionValues[1],
            positionValues[2]
        );

        const rotationFrame = rotationKeys[currentFrame];
        const rotationValues = rotationFrame.values;
        cube.rotation.set(
            rotationValues[0],
            rotationValues[1],
            rotationValues[2]
        );

        object.currentFrame++;
    }

    controls.update();

    renderer.render(scene, camera);
}
