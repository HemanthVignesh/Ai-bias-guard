import { useState, useEffect, useRef } from "react";
import { motion } from "motion/react";
import { Info } from "lucide-react";
import { HeroSection } from "./components/hero-section";
import { InputSection } from "./components/input-section";
import { ResultsDashboard } from "./components/results-dashboard";
import { ArchitecturePanel } from "./components/architecture-panel";
import { FloatingParticles } from "./components/floating-particles";
import { LoadingState } from "./components/loading-state";

interface AnalysisResult {
  biasDetected: boolean;
  confidence: number;
  mitigatedText: string;
  detectedGaps: string[];
  reasoning: string;
  originalText: string;
}

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  // Make sure we are in light mode by default
  useEffect(() => {
    document.documentElement.classList.remove("dark");
  }, []);

  const handleAnalyze = async (text: string) => {
    setIsLoading(true);
    
    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      
      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Failed to analyze text:", error);
      // Optional: Handle error state in UI
    } finally {
      setIsLoading(false);
    }
  };

  // Mock functions to simulate AI model responses
  const detectBias = (text: string): boolean => {
    const biasKeywords = [
      "he", "she", "him", "her", "man", "woman", "boy", "girl",
      "young", "old", "elderly", "guys", "ladies", "chairman",
    ];
    return biasKeywords.some((keyword) =>
      text.toLowerCase().includes(keyword.toLowerCase())
    );
  };

  const calculateConfidence = (text: string): number => {
    const biasKeywords = [
      "he", "she", "him", "her", "man", "woman", "boy", "girl",
      "young", "old", "elderly", "guys", "ladies", "chairman",
    ];
    const matches = biasKeywords.filter((keyword) =>
      text.toLowerCase().includes(keyword.toLowerCase())
    );
    return Math.min(45 + matches.length * 15, 95);
  };

  const generateMitigatedText = (text: string): string => {
    let mitigated = text;
    const replacements: Record<string, string> = {
      "he ": "they ",
      "she ": "they ",
      "him ": "them ",
      "her ": "them ",
      "his ": "their ",
      "hers ": "theirs ",
      "man ": "person ",
      "woman ": "person ",
      "guys": "everyone",
      "ladies": "everyone",
      "chairman": "chairperson",
      "elderly": "older adults",
    };

    Object.entries(replacements).forEach(([biased, neutral]) => {
      const regex = new RegExp(biased, "gi");
      mitigated = mitigated.replace(regex, neutral);
    });

    return mitigated;
  };

  const detectGaps = (text: string): string[] => {
    const gaps: string[] = [];
    
    if (/\b(he|she|him|her)\b/i.test(text)) {
      gaps.push("Gender-specific pronouns detected - consider using gender-neutral alternatives");
    }
    if (/\b(man|woman|boy|girl)\b/i.test(text)) {
      gaps.push("Gender-specific nouns found - could be replaced with inclusive terms");
    }
    if (/\b(young|old|elderly)\b/i.test(text)) {
      gaps.push("Age-related descriptors present - may introduce age bias");
    }
    if (/\b(guys|ladies)\b/i.test(text)) {
      gaps.push("Informal gendered terms identified - use gender-neutral alternatives");
    }
    if (/\bchairman\b/i.test(text)) {
      gaps.push("Gendered job title detected - consider 'chairperson' or 'chair'");
    }

    return gaps.length > 0 ? gaps : ["No significant bias patterns detected"];
  };

  const generateReasoning = (text: string): string => {
    const hasBias = detectBias(text);
    
    if (!hasBias) {
      return "The text appears to use inclusive language without significant bias patterns. The BART model analyzed the content across multiple dimensions including gender, age, race, and cultural references, finding no problematic indicators.";
    }

    return "The BART detection model identified several linguistic patterns that may introduce bias. These include gender-specific pronouns, age descriptors, or gendered terms that could exclude or stereotype certain groups. The T5 mitigation model has generated an alternative version using more inclusive language while preserving the original meaning and context of your text.";
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Floating particles */}
      <FloatingParticles />
      
      {/* Animated background elements */}
      <div className="fixed inset-0 -z-10 bg-slate-50">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-sky-100 via-white to-pink-100 opacity-60" />
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 rounded-full opacity-30"
          style={{
            background: "radial-gradient(circle, #38bdf8 0%, transparent 70%)",
          }}
          animate={{
            x: [0, 50, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-96 h-96 rounded-full opacity-30"
          style={{
            background: "radial-gradient(circle, #f472b6 0%, transparent 70%)",
          }}
          animate={{
            x: [0, -50, 0],
            y: [0, -30, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12">
        {/* Info button */}
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
          onClick={() => setIsPanelOpen(true)}
          className="fixed top-4 right-4 md:top-8 md:right-8 z-30 group"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="absolute -inset-2 bg-gradient-to-r from-sky-400 to-indigo-400 rounded-full opacity-50 group-hover:opacity-75 blur transition duration-300" />
          <div className="relative flex items-center gap-2 px-4 md:px-6 py-2 md:py-3 bg-white/80 backdrop-blur-xl border border-sky-200 rounded-full shadow-lg">
            <Info className="w-4 h-4 md:w-5 md:h-5 text-sky-600" />
            <span className="text-xs md:text-sm font-semibold text-sky-700 hidden sm:inline">Architecture</span>
          </div>
        </motion.button>

        <HeroSection />
        <InputSection onAnalyze={handleAnalyze} isLoading={isLoading} />
        
        {isLoading && <LoadingState />}
        
        {result && !isLoading && (
          <ResultsDashboard
            biasDetected={result.biasDetected}
            confidence={result.confidence}
            mitigatedText={result.mitigatedText}
            detectedGaps={result.detectedGaps}
            reasoning={result.reasoning}
            originalText={result.originalText}
          />
        )}
      </div>

      <ArchitecturePanel isOpen={isPanelOpen} onClose={() => setIsPanelOpen(false)} />

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="relative z-10 text-center py-8 mt-16"
      >
        <div className="text-sm text-muted-foreground">
          <p>Powered by BART (Detection) & T5 (Mitigation) • Fully Local Architecture</p>
          <p className="mt-2 text-xs">No data leaves your device • Privacy-first design</p>
        </div>
      </motion.footer>
    </div>
  );
}

export default App;