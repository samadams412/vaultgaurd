// components/PasswordStrengthBar.tsx
import { motion } from "framer-motion";
import { getPasswordStrength } from "../utils/passwordStrength";
import { CheckCircle, XCircle } from "lucide-react";

type Props = {
  password: string;
};

export default function PasswordStrengthBar({ password }: Props) {
  const { score, rules } = getPasswordStrength(password);

  const barColors = ["bg-red-500", "bg-yellow-400", "bg-blue-500", "bg-green-500", "bg-green-600"];

  return (
    <div className="mt-2">
      <div className="h-2 rounded bg-zinc-800 w-full overflow-hidden mb-2">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(score / 5) * 100}%` }}
          className={`h-2 ${barColors[score - 1] || "bg-zinc-700"} transition-all duration-300`}
        />
      </div>

      <ul className="space-y-1 text-xs text-zinc-400">
        {[
          ["length", "At least 12 characters"],
          ["upper", "1 uppercase letter"],
          ["lower", "1 lowercase letter"],
          ["number", "1 number"],
          ["symbol", "1 special character"],
        ].map(([key, label]) => {
          const passed = rules[key as keyof typeof rules];
          return (
            <motion.li
              key={key}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className={`flex items-center gap-2 ${
                passed ? "text-green-400" : "text-zinc-400"
              }`}
            >
              {passed ? <CheckCircle size={14} /> : <XCircle size={14} />} {label}
            </motion.li>
          );
        })}
      </ul>
    </div>
  );
}
