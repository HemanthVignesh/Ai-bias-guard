import { motion } from "motion/react";
import { useEffect, useState } from "react";

interface BiasGaugeProps {
  confidence: number;
  biasDetected: boolean;
}

export function BiasGauge({ confidence, biasDetected }: BiasGaugeProps) {
  const [animatedValue, setAnimatedValue] = useState(0);

  useEffect(() => {
    const timeout = setTimeout(() => {
      setAnimatedValue(confidence);
    }, 100);
    return () => clearTimeout(timeout);
  }, [confidence]);

  const circumference = 2 * Math.PI * 70;
  const strokeDashoffset = circumference - (animatedValue / 100) * circumference;

  const getColor = () => {
    if (!biasDetected) return "#10b981";
    if (confidence >= 75) return "#ef4444";
    if (confidence >= 50) return "#f59e0b";
    return "#10b981";
  };

  return (
    <div className="relative flex items-center justify-center">
      <svg width="180" height="180" className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx="90"
          cy="90"
          r="70"
          stroke="rgba(139, 92, 246, 0.1)"
          strokeWidth="12"
          fill="none"
        />
        {/* Progress circle */}
        <motion.circle
          cx="90"
          cy="90"
          r="70"
          stroke={getColor()}
          strokeWidth="12"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          style={{
            filter: `drop-shadow(0 0 8px ${getColor()}40)`,
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="text-5xl font-bold"
          style={{ color: getColor() }}
        >
          {Math.round(animatedValue)}%
        </motion.div>
        <div className="text-sm text-muted-foreground mt-1">Confidence</div>
      </div>
    </div>
  );
}
