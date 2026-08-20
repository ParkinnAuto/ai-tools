"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { useGLTF } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

const RobotModel = () => {
  const { scene } = useGLTF("/models/robot.glb");
  const robotRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (!robotRef.current) return;

    robotRef.current.position.y =
      Math.sin(state.clock.elapsedTime * 2) * 0.03;
  });

  return <primitive ref={robotRef} object={scene} scale={3.5} />;
};

const RobotAvatar = () => {
  return (
    <div className="w-full h-[280px] sm:h-[340px] md:h-[380px] lg:h-[420px]">
      <Canvas
        camera={{
          position: [0, 0.5, 5],
          fov: 50,
        }}
      >
        <ambientLight intensity={2} />
        <directionalLight position={[5, 5, 5]} intensity={5} />

        <RobotModel />
      </Canvas>
    </div>
  );
};

export default RobotAvatar;
