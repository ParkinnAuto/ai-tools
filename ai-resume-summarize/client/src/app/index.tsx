import { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import * as DocumentPicker from "expo-document-picker";

import UploadBox from "@/components/UploadBox";
import ResultCard from "@/components/ResultCard";
import { analyzeResume } from "@/services/api";

export default function HomeScreen() {
  const [selectedFile, setSelectedFile] =
    useState<DocumentPicker.DocumentPickerAsset | null>(null);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const pickFile = async () => {
    try {
      const response = await DocumentPicker.getDocumentAsync({
        type: [
          "application/pdf",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          "text/plain",
        ],
        copyToCacheDirectory: true,
      });

      if (response.canceled) return;

      setSelectedFile(response.assets[0]);
      setResult(null);
    } catch (error) {
      Alert.alert("Error", "Failed to pick file.");
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      Alert.alert("No file selected", "Please upload a resume first.");
      return;
    }

    try {
      setLoading(true);

      let fileForUpload: any;

      if (Platform.OS === "web") {
        // On web, Expo DocumentPicker provides the real browser File object here
        fileForUpload = selectedFile.file;
      } else {
        // On mobile, use uri/name/type format
        fileForUpload = {
          uri: selectedFile.uri,
          name: selectedFile.name,
          type: selectedFile.mimeType || "application/octet-stream",
        };
      }

      const data = await analyzeResume(fileForUpload);

      setResult(data.analysis);
    } catch (error: any) {
      console.log(error.response?.data || error.message);
      Alert.alert(
        "Analyze failed",
        "Something went wrong while analyzing the resume.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.logo}>CKQ</Text>

          <Text style={styles.title}>Minimal Resume Analysis for HR</Text>
        </View>

        <UploadBox fileName={selectedFile?.name} onPickFile={pickFile} />

        <Pressable
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleAnalyze}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.buttonText}>Analyze Resume</Text>
          )}
        </Pressable>

        <ResultCard analysis={result} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#FAFAFF",
  },
  container: {
    width: "100%",
    maxWidth: 860,
    alignSelf: "center",
    paddingHorizontal: 24,
    paddingTop: 54,
    paddingBottom: 72,
  },
  header: {
    alignItems: "center",
    marginBottom: 14,
  },
  badge: {
    backgroundColor: "#EDE9FE",
    paddingHorizontal: 14,
    paddingVertical: 7,
    borderRadius: 999,
    marginBottom: 18,
  },
  badgeText: {
    color: "#5B21B6",
    fontSize: 13,
    fontWeight: "700",
  },
  logo: {
    fontSize: 52,
    fontWeight: "900",
    color: "#4C1D95",
    letterSpacing: -1.5,
  },
  title: {
    marginTop: 14,
    fontSize: 28,
    fontWeight: "900",
    color: "#111827",
    textAlign: "center",
  },
  subtitle: {
    marginTop: 12,
    fontSize: 15,
    lineHeight: 23,
    color: "#6B7280",
    textAlign: "center",
    maxWidth: 560,
  },
  button: {
    marginTop: 22,
    backgroundColor: "#6D28D9",
    height: 56,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#6D28D9",
    shadowOpacity: 0.2,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 8 },
    elevation: 4,
  },
  buttonDisabled: {
    opacity: 0.65,
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "800",
  },
});
