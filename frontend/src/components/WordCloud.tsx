import { useRef, useMemo } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Text, OrbitControls } from "@react-three/drei"
import * as THREE from "three"
import type { WordWeight } from "../types"

interface WordCloudProps {
  words: WordWeight[]
}

interface WordProps {
  word: string
  weight: number
  position: [number, number, number]
}

function Word({ word, weight, position }: WordProps) {
  const ref = useRef<any>(null)
  const worldPos = useMemo(() => new THREE.Vector3(), [])

  const color = useMemo(() => {
    // Lerp color from blue (low weight) to pink (high weight)
    const low = new THREE.Color("#60a5fa")
    const high = new THREE.Color("#f472b6")
    return low.lerp(high, weight).getStyle()
  }, [weight])

  const fontSize = Math.min(0.2 + weight * 0.6, 0.6)

  useFrame(({ camera }) => {
    if (ref.current) {
      ref.current.lookAt(camera.position)
      ref.current.getWorldPosition(worldPos)
      const dist = worldPos.distanceTo(camera.position)

      // Fade words based on distance to create depth perception
      const opacity = THREE.MathUtils.mapLinear(dist, 4.5, 10, 1, 0)
      
      ref.current.fillOpacity = THREE.MathUtils.clamp(opacity, 0, 1)
      ref.current.outlineOpacity = THREE.MathUtils.clamp(opacity, 0, 1)
    }
  })

  return (
    <Text
      ref={ref}
      position={position}
      fontSize={fontSize}
      color={color}
      anchorX="center"
      anchorY="middle"
      outlineWidth={0.01}
      outlineColor="#000000"
    >
      {word}
    </Text>
  )
}

function Cloud({ words }: { words: WordWeight[] }) {
  const groupRef = useRef<THREE.Group>(null)

  const positions = useMemo(() => {
    return words.map((_, i) => {
      // Fibonacci sphere distribution for even spacing across the globe
      const phi = Math.acos(1 - (2 * (i + 0.5)) / words.length)
      const theta = Math.PI * (1 + Math.sqrt(5)) * i
      const radius = 3.5
      return [
        radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.sin(phi) * Math.sin(theta),
        radius * Math.cos(phi),
      ] as [number, number, number]
    })
  }, [words])

  useFrame((_state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += delta * 0.12
    }
  })

  return (
    <group ref={groupRef}>
      {words.map((w, i) => (
        <Word
          key={`${w.word}-${i}`}
          word={w.word}
          weight={w.weight}
          position={positions[i]}
        />
      ))}
    </group>
  )
}

export default function WordCloud({ words }: WordCloudProps) {
  return (
    <div className="w-full h-[600px]"> 
      <Canvas 
        camera={{ position: [0, 0, 8], fov: 60 }}
        gl={{ alpha: true, antialias: true }} 
        onCreated={({ gl }) => {
          gl.setClearColor(0x000000, 0) 
        }}
      >
        <fog attach="fog" args={["#030712", 5, 12]} />
        
        <ambientLight intensity={1} />
        <Cloud words={words} />
        
        <OrbitControls 
          enableZoom={false}
          enablePan={false} 
        />
      </Canvas>
    </div>
  )
}