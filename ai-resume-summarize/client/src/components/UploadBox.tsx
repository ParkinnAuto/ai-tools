import { Pressable, StyleSheet, Text, View } from "react-native";

type UploadBoxProps = {
  fileName?: string;
  onPickFile: () => void;
};

export default function UploadBox({ fileName, onPickFile }: UploadBoxProps) {
  return (
    <Pressable style={styles.container} onPress={onPickFile}>
      <View style={styles.iconBox}>
        <Text style={styles.icon}>📄</Text>
      </View>

      <Text style={styles.title}>
        {fileName ? "Resume Selected" : "Upload Resume / CV"}
      </Text>

      <Text style={styles.subtitle}>
        {fileName || "PDF, DOCX, or TXT file"}
      </Text>

      <Text style={styles.helperText}>
        Click here to choose a file from your device
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
    borderWidth: 1.5,
    borderColor: "#C4B5FD",
    borderStyle: "dashed",
    borderRadius: 26,
    paddingVertical: 34,
    paddingHorizontal: 24,
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    marginTop: 30,
    shadowColor: "#6D28D9",
    shadowOpacity: 0.06,
    shadowRadius: 18,
    shadowOffset: { width: 0, height: 8 },
    elevation: 2,
  },
  iconBox: {
    width: 64,
    height: 64,
    borderRadius: 22,
    backgroundColor: "#EDE9FE",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  },
  icon: {
    fontSize: 31,
  },
  title: {
    fontSize: 19,
    fontWeight: "900",
    color: "#4C1D95",
    marginBottom: 7,
    textAlign: "center",
  },
  subtitle: {
    fontSize: 14,
    color: "#6B7280",
    textAlign: "center",
  },
  helperText: {
    marginTop: 12,
    fontSize: 13,
    color: "#8B5CF6",
    fontWeight: "600",
    textAlign: "center",
  },
});